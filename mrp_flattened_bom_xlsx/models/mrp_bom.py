# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'

    def _get_flattened_totals(self, factor=1, totals=None):
        """
        Generate a summary of product quantities as a dict of flattened BOM
        """
        if totals is None:
            totals = {}
        for line in self.bom_line_ids:
            sub_bom = self._bom_find(product=line.product_id)
            if sub_bom:
                factor *= line.product_uom_id._compute_quantity(
                    line.product_qty, line.product_id.uom_id)
                sub_bom._get_flattened_totals(factor, totals)
            else:
                factor /= self.product_uom_id._compute_quantity(
                    self.product_qty, self.product_uom_id)
                if totals.get(line.product_id):
                    totals[line.product_id] += line.product_uom_id. \
                        _compute_quantity(
                        line.product_qty * factor, line.product_id.uom_id)
                else:
                    totals[line.product_id] = line.product_uom_id. \
                        _compute_quantity(
                        line.product_qty * factor, line.product_id.uom_id)
        return totals
