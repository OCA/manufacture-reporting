# Copyright 2018 Camptocamp SA
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class BomRouteCurrentStock(models.TransientModel):
    _name = "mrp.bom.current.stock"
    _description = 'MRP Bom Route Current Stock'

    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="Starting Bill of Materials",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product Variant',
        domain="[('type', 'in', ['product', 'consu'])]",
        required=True,
    )
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        related='product_id.product_tmpl_id',
    )
    product_qty = fields.Float(
        related='bom_id.product_qty',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        related="bom_id.product_uom_id",
    )
    qty_able_to_produce = fields.Float(
        string="Quantity Able to Produce Immediately",
        compute="_compute_available_qty",
        help="This is the quantity of top level product that can be "
             "manufactured directly with only one production order without "
             "the need of any extra operation, i.e., taking into account only"
             "level 1."
    )
    total_qty_able_to_produce = fields.Float(
        string="Total Quantity Able to Produce",
        compute="_compute_available_qty",
        help="This is the quantity of top level product that can be "
             "manufactured with what is currently on stock taking into account"
             "all components in the BoM."
    )
    location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Starting location",
    )
    line_ids = fields.One2many(
        comodel_name='mrp.bom.current.stock.line',
        inverse_name='explosion_id',
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.bom_id = self.env['mrp.bom']._bom_find(
            product=self.product_id,
        )

    @api.onchange('bom_id')
    def _onchange_bom_id(self):
        if self.bom_id.location_id:
            self.location_id = self.bom_id.location_id

    @api.model
    def _prepare_line(self, bom_line, level, factor):
        return {
            'product_id': bom_line.product_id.id,
            'bom_line': bom_line.id,
            'bom_level': level,
            'product_qty': bom_line.product_qty * factor,
            'product_uom_id': bom_line.product_uom_id.id,
            'location_id': (bom_line.location_id.id
                            if bom_line.location_id else self.location_id.id),
            'explosion_id': self.id,
        }

    @api.multi
    def do_explode(self):
        self.ensure_one()
        line_obj = self.env['mrp.bom.current.stock.line']

        def _create_lines(bom, level=0, factor=1):
            level += 1
            for line in bom.bom_line_ids:
                vals = self._prepare_line(line, level, factor)
                line_obj.create(vals)
                location = line.location_id
                line_boms = line.product_id.bom_ids
                boms = line_boms.filtered(
                    lambda bom: bom.location_id == location
                ) or line_boms
                if boms:
                    line_qty = line.product_uom_id._compute_quantity(
                        line.product_qty,
                        boms[0].product_uom_id,
                    )
                    new_factor = factor * line_qty / boms[0].product_qty
                    _create_lines(boms[0], level, new_factor)

        _create_lines(self.bom_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open lines',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'mrp.bom.current.stock',
            'view_id': self.env.ref(
                'mrp_bom_current_stock.mrp_bom_current_stock_view_form2'
            ).id,
            'target': 'new',
            'res_id': self.id,
        }

    @api.onchange("line_ids")
    def _compute_available_qty(self):
        max_level = max(self.line_ids.mapped("bom_level"))
        product_available = self.product_id.with_context(
            location=self.location_id.id
        )._product_available()[self.product_id.id]['qty_available']
        on_hand_qty = self.product_id.product_tmpl_id.uom_id._compute_quantity(
            product_available,
            self.product_uom_id,
        )
        last_bom_id = self.bom_id.id
        for level in range(1, max_level+1):
            minimum_qty = False
            for line in self.line_ids.filtered(
                lambda x: x.bom_level == level and x.bom_id.id == last_bom_id
            ):
                line_qty = line.qty_available_in_source_loc / line.product_qty
                if isinstance(minimum_qty, bool) or line_qty < minimum_qty:
                    minimum_qty = line_qty
                    bom_id = list(
                        set(line.product_id.bom_ids.ids) &
                        set(self.line_ids.mapped("bom_id").ids)
                    )
                    if bom_id:
                        last_bom_id = bom_id[0]
            on_hand_qty += minimum_qty
            if level == 1:
                self.qty_able_to_produce = on_hand_qty
        self.total_qty_able_to_produce = on_hand_qty


class BomRouteCurrentStockLine(models.TransientModel):
    _name = "mrp.bom.current.stock.line"
    _description = 'MRP Bom Route Current Stock Line'

    explosion_id = fields.Many2one(
        comodel_name='mrp.bom.current.stock',
        readonly=True
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product Variant',
        readonly=True,
    )
    bom_level = fields.Integer(
        string='BoM Level',
        readonly=True
    )
    product_qty = fields.Float(
        string='Product Quantity',
        readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
    )
    product_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Product Unit of Measure',
        readonly=True,
    )
    location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Source location",
    )
    bom_line = fields.Many2one(
        comodel_name="mrp.bom.line",
        string="BoM line",
        redonly=True
    )
    qty_available_in_source_loc = fields.Float(
        string="Qty Available in Source",
        compute="_compute_qty_available_in_source_loc",
        redonly=True
    )
    bom_id = fields.Many2one(comodel_name="mrp.bom", string="Parent BoM",
                             related='bom_line.bom_id', redonly=True)

    @api.multi
    @api.onchange('location_id')
    def _compute_qty_available_in_source_loc(self):
        for record in self:
            product_available = record.product_id.with_context(
                location=record.location_id.id
            )._product_available()[record.product_id.id]['qty_available']
            res = record.product_id.product_tmpl_id.uom_id._compute_quantity(
                product_available,
                record.product_uom_id,
            )
            record.qty_available_in_source_loc = res
