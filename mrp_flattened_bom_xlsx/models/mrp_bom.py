# Copyright 2018 ForgeFlow S.L.
#   (http://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class MrpBom(models.Model):
    """Defines bills of material for a product or a product template"""

    _inherit = "mrp.bom"

    def _get_flattened_totals(self, factor=1, totals=None):
        """Calculate the unitary product requirements of flattened BOM."""
        self.ensure_one()
        if totals is None:
            totals = {}
        if not self.product_qty:
            return totals
        factor /= self.product_uom_id._compute_quantity(
            self.product_qty, self.product_tmpl_id.uom_id, round=False
        )
        boms = self.env["mrp.bom"]._bom_find(self.bom_line_ids.product_id)
        for line in self.bom_line_ids:
            qty = factor * line.product_uom_id._compute_quantity(
                line.product_qty, line.product_id.uom_id, round=False
            )
            sub_bom = boms.get(line.product_id)
            if sub_bom:
                sub_bom._get_flattened_totals(qty, totals)
            else:
                totals[line.product_id] = totals.get(line.product_id, 0.0) + qty
        return totals
