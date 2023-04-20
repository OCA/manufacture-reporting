# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

from odoo.addons import decimal_precision as dp

UNIT = dp.get_precision("Product Price")


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    labour_cost = fields.Float(
        string="Labour Cost", compute="_compute_labour_cost", digits=UNIT
    )

    def _compute_labour_cost(self):
        for bom in self:
            cost = 0.0
            for operation in bom.operation_ids:
                cost += operation.workcenter_id.costs_hour * (
                    operation.time_cycle / 60.0
                )
            bom.labour_cost = cost
