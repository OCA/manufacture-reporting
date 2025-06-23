# Copyright 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_quantity_by_lot(self):
        self.ensure_one()
        if self.product_id.tracking != "lot":
            return {}
        quantity_by_lot = defaultdict(float)
        for move_line in self.move_line_ids.filtered(lambda ml: ml.state == "done"):
            quantity_by_lot[
                move_line.lot_id or False
            ] += move_line.product_uom_id._compute_quantity(
                move_line.qty_done,
                self.product_uom,
            )
        return quantity_by_lot
