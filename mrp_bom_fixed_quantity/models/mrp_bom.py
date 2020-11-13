# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    def explode(self, product, quantity, picking_type=False):
        """
            Description: After the original explode is ran set the quantity of
            BOM lines back to it's original quantity if fixed_quantity is set
            to True.

            NOTE: qty and original_qty are both updated by quantity
        """
        res = super().explode(product, quantity, picking_type)
        # loop through every tuple in the dictionary(lines_done)
        for bom_line_tuple in res[1]:
            # Rename variables for better readbility
            bom_line_obj = bom_line_tuple[0]
            bom_line_dictionary = bom_line_tuple[1]
            if bom_line_obj.fixed_quantity:
                # update the dictionary key value for qty and original_qty
                bom_line_dictionary["qty"] = bom_line_obj.product_qty
                bom_line_dictionary["original_qty"] = bom_line_obj.product_qty
        # res contains boms_done, lines_done
        return res
