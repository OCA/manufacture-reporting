# Copyright 2018 Camptocamp SA
# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BomRouteCurrentStock(models.TransientModel):
    _name = "mrp.bom.current.stock"
    _description = "MRP Bom Route Current Stock"

    bom_id = fields.Many2one(
        comodel_name="mrp.bom", string="Starting Bill of Materials", required=True
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product Variant",
        domain="[('type', 'in', ['product', 'consu'])]",
        required=True,
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
        related="product_id.product_tmpl_id",
    )
    product_qty = fields.Float(
        related="bom_id.product_qty", digits="Product Unit of Measure"
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom", related="bom_id.product_uom_id"
    )
    location_id = fields.Many2one(
        comodel_name="stock.location", string="Starting location"
    )
    line_ids = fields.One2many(
        comodel_name="mrp.bom.current.stock.line",
        inverse_name="explosion_id",
        domain=[("show_line", "=", True)],
    )
    desired_quantity = fields.Integer(string="Product Quantity", default=1)
    availability = fields.Selection(
        [("available", "Available"), ("not available", "Not Available")],
        default="not available",
    )

    potencial_qty = fields.Integer(default=0, string="Potencial Quantity")

    explosion_type = fields.Selection(
        [("all", "All"), ("mo_recreation", "MO Recreation")], default="all"
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.bom_id = self.env["mrp.bom"]._bom_find(product_tmpl=self.product_id)

    @api.onchange("bom_id")
    def _onchange_bom_id(self):
        if self.bom_id.location_id:
            self.location_id = self.bom_id.location_id

    @api.model
    def _prepare_line(self, bom_line, level, factor):
        return {
            "product_id": bom_line.product_id.id,
            "bom_line": bom_line.id,
            "bom_level": level,
            "product_qty": bom_line.product_qty * factor,
            "product_uom_id": bom_line.product_uom_id.id,
            "location_id": (
                bom_line.location_id.id if bom_line.location_id else self.location_id.id
            ),
            "explosion_id": self.id,
            "show_line": self.explosion_type == "all"
            or bom_line.child_bom_id.type != "phantom",
        }

    def _create_lines(self, bom, level=0, factor=1):

        line_obj = self.env["mrp.bom.current.stock.line"]
        level += 1
        for line in bom.bom_line_ids:
            vals = self._prepare_line(line, level, factor)
            line_obj.create(vals)
            location = line.location_id
            line_boms = line.product_id.bom_ids
            boms = (
                line_boms.filtered(lambda bom: bom.location_id == location) or line_boms
            )
            if boms:
                line_qty = line.product_uom_id._compute_quantity(
                    line.product_qty, boms[0].product_uom_id
                )
                new_factor = factor * line_qty / boms[0].product_qty
                if self.explosion_type == "all" or (
                    self.explosion_type == "mo_recreation"
                    and line.child_bom_id.type == "phantom"
                ):
                    self._create_lines(boms[0], level, new_factor)

    def do_explode(self):
        self.ensure_one()
        self._create_lines(self.bom_id, factor=self.desired_quantity)
        self.compute_potencial_qty()
        return {
            "type": "ir.actions.act_window",
            "name": "Open lines",
            "view_mode": "form",
            "res_model": "mrp.bom.current.stock",
            "view_id": self.env.ref(
                "mrp_bom_current_stock.mrp_bom_current_stock_view_form2"
            ).id,
            "target": "new",
            "res_id": self.id,
        }

    def compute_potencial_qty(self):
        level_1_lines = self.line_ids.search(
            [("explosion_id", "=", self.id), ("bom_level", "=", 1)]
        )
        min_availability = 999999
        for line in level_1_lines:
            line_availability = line.potencial_qty(factor=self.desired_quantity)
            if min_availability > line_availability:
                min_availability = line_availability
        self.potencial_qty = min_availability
        if self.potencial_qty > self.desired_quantity:
            self.availability = "available"
        else:
            self.availability = "not available"

    def action_go_back(self):
        action = self.env.ref("mrp_bom_current_stock.mrp_bom_current_stock_action")
        res = action.sudo().read()[0]
        res["context"] = {
            "default_bom_id": self.bom_id.id,
            "default_product_id": self.product_id.id,
            "default_desired_quantity": self.desired_quantity,
            "default_explosion_type": self.explosion_type,
        }
        return res


class BomRouteCurrentStockLine(models.TransientModel):
    _name = "mrp.bom.current.stock.line"
    _description = "MRP Bom Route Current Stock Line"

    explosion_id = fields.Many2one(comodel_name="mrp.bom.current.stock", readonly=True)
    show_line = fields.Boolean()
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product Variant", readonly=True
    )
    bom_level = fields.Integer(string="BoM Level", readonly=True)
    product_qty = fields.Float(
        string="Product Quantity",
        readonly=True,
        digits="Product Unit of Measure",
        default=1,
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom", string="Product Unit of Measure", readonly=True
    )
    location_id = fields.Many2one(
        comodel_name="stock.location", string="Source location"
    )
    bom_line = fields.Many2one(
        comodel_name="mrp.bom.line", string="BoM line", readonly=True
    )
    qty_available_in_source_loc = fields.Float(
        string="Qty Available in Source",
        compute="_compute_qty_available_in_source_loc",
        readonly=True,
    )
    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="Parent BoM",
        related="bom_line.bom_id",
        readonly=True,
    )

    explosion_type = fields.Selection(related="explosion_id.explosion_type", store=True)

    availability = fields.Selection(
        [("available", "Available"), ("not available", "Not Available")],
        default="not available",
    )

    @api.onchange("location_id")
    def _compute_qty_available_in_source_loc(self):
        for record in self:
            product_available = record.product_id.with_context(
                location=record.location_id.id
            )._product_available()[record.product_id.id]["qty_available"]
            res = record.product_id.product_tmpl_id.uom_id._compute_quantity(
                product_available, record.product_uom_id
            )
            record.qty_available_in_source_loc = res

    def potencial_qty(self, level=0, factor=1):
        level += 1
        boms = self.product_id.bom_ids
        if (boms and self.explosion_type == "all") or (
            self.explosion_type == "mo_recreation"
            and self.bom_line.child_bom_id.type == "phantom"
        ):
            min_availability = 999999
        else:
            min_availability = 0
        line_obj = self.env["mrp.bom.current.stock.line"]
        if self.explosion_type == "all" or (
            self.explosion_type == "mo_recreation"
            and self.bom_line.child_bom_id.type == "phantom"
        ):
            for line in boms.bom_line_ids:
                bom_line = line_obj.search(
                    [
                        ("product_id", "=", line.product_id.id),
                        ("bom_line", "=", line.id),
                        ("bom_level", "=", level + 1),
                        ("product_uom_id", "=", line.product_uom_id.id),
                        (
                            "explosion_id",
                            "=",
                            self.explosion_id.id,
                        ),
                    ]
                )
                line_availability = bom_line.potencial_qty(level=level, factor=factor)
                if min_availability > line_availability:
                    min_availability = line_availability

        if self.qty_available_in_source_loc + min_availability >= self.product_qty:
            self.availability = "available"
        if self.product_qty // factor == 0:
            return 0
        if self.bom_line.child_bom_id.type == "phantom":
            return min_availability // (self.product_qty // factor)
        return (min_availability + self.qty_available_in_source_loc) // (
            self.product_qty // factor
        )
