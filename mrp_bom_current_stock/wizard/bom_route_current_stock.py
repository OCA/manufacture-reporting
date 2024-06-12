# Copyright 2018 Camptocamp SA
# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import math

from odoo import api, fields, models


class BomRouteCurrentStock(models.TransientModel):
    _name = "mrp.bom.current.stock"
    _description = "MRP Bom Route Current Stock"

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
    bom_id = fields.Many2one(
        comodel_name="mrp.bom", string="Starting Bill of Materials", required=True
    )
    product_qty = fields.Float(
        related="bom_id.product_qty", digits="Product Unit of Measure"
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom", related="bom_id.product_uom_id"
    )
    location_id = fields.Many2one(
        comodel_name="stock.location", string="Source location"
    )
    exclude_location_ids = fields.Many2many(
        comodel_name="stock.location",
        string="Exclude locations",
        domain="[('id', 'child_of', location_id), ('id', '!=', location_id)]",
        help="Select only the parent location you want to exclude.",
    )
    line_ids = fields.One2many(
        comodel_name="mrp.bom.current.stock.line",
        inverse_name="wizard_id",
    )
    explosion_type = fields.Selection(
        [("one", "One Level"), ("all", "All Levels")], default="all"
    )
    desired_qty = fields.Integer(string="Desired Quantity", default=1)
    qty_available_in_source_loc = fields.Float(
        string="Qty Available in Source",
        compute="_compute_qty_available_in_source_loc",
        store=True,
    )
    potential_qty = fields.Float()
    potential_qty_rounded = fields.Integer(
        string="Potential Quantity",
        help="Potential quantity that could be manufactured given all current "
        "on-hand stock at the specified locations.",
        compute="_compute_potential_qty_rounded",
        store="True",
    )
    availability = fields.Selection(
        [("available", "Available"), ("not_available", "Not Available")],
        compute="_compute_availability",
        store=True,
        help="The field shows the availability that you have taking into "
        "account the potential quantity that could end up being manufactured.",
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.bom_id = self.env["mrp.bom"]._bom_find(product=self.product_id)

    def _get_exclude_locations_qty(self, product_id, location_id):
        qty = 0
        for exclude_location_id in self.exclude_location_ids:
            if exclude_location_id.is_sublocation_of(location_id):
                qty += product_id.with_context(
                    location=exclude_location_id.id
                ).qty_available
        return qty

    def _get_outgoing_reservation_qty(self, product_id, location_id):
        # Copy of stock.buffer.`_get_outgoing_reservation_qty` method.
        domain = [
            ("product_id", "=", product_id.id),
            ("state", "in", ("partially_available", "assigned")),
        ]
        lines = self.env["stock.move.line"].search(domain)
        lines = lines.filtered(
            lambda line: line.location_id.is_sublocation_of(location_id)
            and not line.location_id.is_sublocation_of(self.exclude_location_ids)
            and (
                not line.location_dest_id.is_sublocation_of(location_id)
                or line.location_dest_id.is_sublocation_of(self.exclude_location_ids)
            )
        )
        return sum(lines.mapped("product_qty"))

    @api.depends("product_id", "location_id")
    def _compute_qty_available_in_source_loc(self):
        for rec in self:
            available_qty = 0
            if rec.bom_id.type != "phantom":
                available_qty = rec.product_id.with_context(
                    location=rec.location_id.id
                ).qty_available
                available_qty -= rec._get_outgoing_reservation_qty(
                    rec.product_id,
                    rec.location_id,
                )
                available_qty -= rec._get_exclude_locations_qty(
                    rec.product_id,
                    rec.location_id,
                )
                available_qty = rec.product_id.product_tmpl_id.uom_id._compute_quantity(
                    available_qty, rec.product_uom_id
                )
            rec.qty_available_in_source_loc = available_qty

    @api.depends("potential_qty")
    def _compute_availability(self):
        for rec in self:
            rec.availability = (
                "available" if rec.potential_qty >= rec.desired_qty else "not_available"
            )

    @api.depends("potential_qty")
    def _compute_potential_qty_rounded(self):
        for rec in self:
            rec.potential_qty_rounded = math.floor(rec.potential_qty)

    @api.model
    def _prepare_line(self, bom_line, level, factor):
        return {
            "bom_line_id": bom_line.id,
            "bom_level": level,
            "product_qty": bom_line.product_qty * factor,
            "location_id": self.location_id.id,
            "wizard_id": self.id,
        }

    def _create_lines(self, bom, level, factor):
        line_obj = self.env["mrp.bom.current.stock.line"]
        level += 1
        for bom_line in bom.bom_line_ids:
            line_vals = self._prepare_line(bom_line, level, factor)
            line = line_obj.create(line_vals)
            if line.bom_id:
                line_qty = line.product_uom_id._compute_quantity(
                    line.product_qty, line.bom_id.product_uom_id
                )
                new_factor = (
                    factor * line_qty / (line.bom_id.product_qty * self.desired_qty)
                )
                if self.explosion_type == "all" or (
                    self.explosion_type == "one" and line.bom_id.type == "phantom"
                ):
                    self._create_lines(line.bom_id, level, new_factor)

    def do_explode(self):
        self.ensure_one()
        self._create_lines(self.bom_id, 0, self.desired_qty)
        self.potential_qty = self.compute_potential_qty(self, self.bom_id, 0)
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

    def compute_potential_qty(self, rec, bom, level):
        lines = self.line_ids.filtered(
            lambda x: x.parent_bom_id.id == bom.id and x.bom_level == level + 1
        )
        potential_quantities = []
        for line in lines:
            potential_quantity = 0
            if line.bom_id and (
                self.explosion_type != "one" or line.bom_id.type == "phantom"
            ):
                potential_quantity = self.compute_potential_qty(
                    line, line.bom_id, level + 1
                )
            elif line.product_qty != 0:
                potential_quantity = line.qty_available_in_source_loc / (
                    line.product_qty / self.desired_qty
                )
            potential_quantities.append(potential_quantity)
        qty = (
            min(potential_quantities) + rec.qty_available_in_source_loc
            if potential_quantities
            else rec.qty_available_in_source_loc
        )
        return qty

    def action_go_back(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "mrp_bom_current_stock.mrp_bom_current_stock_action"
        )
        action["context"] = {
            "default_bom_id": self.bom_id.id,
            "default_product_id": self.product_id.id,
            "default_location_id": self.location_id.id,
            "default_exclude_location_ids": self.exclude_location_ids.ids,
            "default_desired_qty": self.desired_qty,
            "default_explosion_type": self.explosion_type,
        }
        return action


class BomRouteCurrentStockLine(models.TransientModel):
    _name = "mrp.bom.current.stock.line"
    _description = "MRP Bom Route Current Stock Line"
    _order = "bom_level, parent_bom_id"

    wizard_id = fields.Many2one(comodel_name="mrp.bom.current.stock", readonly=True)
    bom_level = fields.Integer(string="BoM Level", readonly=True)
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product Variant",
        related="bom_line_id.product_id",
        readonly=True,
    )
    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="BoM",
        compute="_compute_bom_id",
        store=True,
        readonly=True,
    )
    bom_type = fields.Selection(
        related="bom_id.type",
        readonly=True,
    )
    bom_line_id = fields.Many2one(
        comodel_name="mrp.bom.line", string="BoM line", readonly=True
    )
    explosion_type = fields.Selection(related="wizard_id.explosion_type", store=True)
    product_qty = fields.Float(
        string="Product Quantity",
        readonly=True,
        digits="Product Unit of Measure",
        default=1,
    )
    qty_available_in_source_loc = fields.Float(
        string="Qty Available in Source",
        compute="_compute_qty_available_in_source_loc",
        digits="Product Unit of Measure",
    )
    potential_qty = fields.Float(
        string="Potential Quantity",
        help="Potential quantity that could be manufactured given all current "
        "on-hand stock at the specified locations.",
        digits="Product Unit of Measure",
        compute="_compute_potential_qty",
        store=True,
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Product Unit of Measure",
        related="bom_line_id.product_uom_id",
    )
    availability = fields.Selection(
        [("available", "Available"), ("not_available", "Not Available")],
        compute="_compute_availability",
        help="The field shows the availability that you have taking into "
        "account the available quantity that could end up being manufactured.",
    )
    parent_bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="Parent BoM",
        related="bom_line_id.bom_id",
    )
    location_id = fields.Many2one(
        comodel_name="stock.location", string="Source location"
    )

    @api.onchange("location_id")
    def _compute_qty_available_in_source_loc(self):
        for rec in self:
            available_qty = 0
            if rec.bom_id.type != "phantom":
                available_qty = rec.product_id.with_context(
                    location=rec.location_id.id
                ).qty_available
                available_qty -= rec.wizard_id._get_outgoing_reservation_qty(
                    rec.product_id,
                    rec.location_id,
                )
                available_qty -= rec.wizard_id._get_exclude_locations_qty(
                    rec.product_id,
                    rec.location_id,
                )
                available_qty = rec.product_id.product_tmpl_id.uom_id._compute_quantity(
                    available_qty, rec.product_uom_id
                )
            rec.qty_available_in_source_loc = available_qty

    @api.depends("bom_line_id")
    def _compute_bom_id(self):
        for rec in self:
            boms = rec.bom_line_id.product_id.bom_ids
            rec.bom_id = boms[0] if boms else None

    @api.depends("product_qty", "qty_available_in_source_loc")
    def _compute_availability(self):
        for rec in self:
            rec.availability = (
                "available" if rec.potential_qty >= rec.product_qty else "not_available"
            )

    @api.depends("qty_available_in_source_loc")
    def _compute_potential_qty(self):
        for rec in self:
            rec.potential_qty = (
                rec.wizard_id.compute_potential_qty(rec, rec.bom_id, rec.bom_level)
                if rec.bom_id
                else rec.qty_available_in_source_loc
            )
