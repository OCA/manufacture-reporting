# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'

    @api.multi
    def _get_flattened_totals(self, factor=1, totals=None):
        """Calculate the **unitary** product requirements of flattened BOM.
        *Unit* means that the requirements are computed for one unit of the
        default UoM of the product.
        :returns: dict: keys are components and values are aggregated quantity
        in the product default UoM.
        """
        self.ensure_one()
        if totals is None:
            totals = {}
        factor /= self.product_uom_id._compute_quantity(
            self.product_qty, self.product_tmpl_id.uom_id, round=False)
        for line in self.bom_line_ids:
            sub_bom = self._bom_find(product=line.product_id)
            if sub_bom:
                new_factor = factor * line.product_uom_id._compute_quantity(
                    line.product_qty, line.product_id.uom_id, round=False)
                sub_bom._get_flattened_totals(new_factor, totals)
            else:
                if totals.get(line.product_id):
                    totals[line.product_id] += factor * \
                        line.product_uom_id._compute_quantity(
                            line.product_qty,
                            line.product_id.uom_id,
                            round=False)
                else:
                    totals[line.product_id] = factor * \
                        line.product_uom_id._compute_quantity(
                            line.product_qty,
                            line.product_id.uom_id,
                            round=False)
        return totals
