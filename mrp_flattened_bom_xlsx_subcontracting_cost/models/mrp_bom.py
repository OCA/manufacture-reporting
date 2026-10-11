# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    subcontracting_cost = fields.Float(
        compute="_compute_subcontracting_cost",
        digits="Product Price",
    )

    def _compute_subcontracting_cost(self):
        supplier_info_obj = self.env["product.supplierinfo"]
        for bom in self:
            if bom.type == "subcontract" and bom.subcontractor_ids:
                supplier_info = supplier_info_obj.search(
                    [
                        ("partner_id", "=", bom.subcontractor_ids[0].id),
                        ("product_tmpl_id", "=", bom.product_tmpl_id.id),
                    ],
                    limit=1,
                )
                bom.subcontracting_cost = supplier_info.price
            else:
                bom.subcontracting_cost = 0.0
