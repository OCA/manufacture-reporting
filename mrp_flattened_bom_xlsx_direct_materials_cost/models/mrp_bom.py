# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    direct_materials_cost = fields.Float(
        string="Direct Material Cost",
        compute="_compute_direct_materials_cost",
        digits="Product Price",
    )

    def _compute_direct_materials_cost(self):
        for bom in self:
            price = 0.0
            starting_factor = bom.product_uom_id._compute_quantity(
                bom.product_qty, bom.product_tmpl_id.uom_id, round=False
            )
            totals = bom._get_flattened_totals(factor=starting_factor)
            for product, total_qty in totals.items():
                price += total_qty * product._get_direct_material_unit_cost()
            bom.direct_materials_cost = price
