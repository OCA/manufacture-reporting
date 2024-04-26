# © Copyright 2017-2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MRPBomStructureReportLevel1(models.AbstractModel):
    _name = "report.mrp_bom_structure_report_level_1.mrp_bs_l1"
    _inherit = "report.mrp.report_bom_structure"
    _description = "BOM Structure Report Level 1"

    def _get_pdf_line(
        self, bom_id, product_id=False, qty=1, unfolded_ids=None, unfolded=False
    ):
        if unfolded_ids is None:
            unfolded_ids = set()

        bom = self.env["mrp.bom"].browse(bom_id)
        product = (
            self.env["product.product"].browse(product_id)
            if product_id
            else bom.product_id or bom.product_tmpl_id.product_variant_id
        )
        warehouse_id = (
            self.env.context.get("warehouse") or self.get_warehouses()[0]["id"]
        )
        warehouse = self.env["stock.warehouse"].browse(warehouse_id)

        data = self._get_bom_data(
            bom, warehouse, product=product, line_qty=qty, level=0
        )
        pdf_lines = self._get_bom_array_lines(data, 1, unfolded_ids, unfolded, True)

        data["components"] = []
        data["lines"] = pdf_lines
        return data

    @api.model
    def _get_bom_array_lines(
        self, data, level, unfolded_ids, unfolded, parent_unfolded=True
    ):
        bom_lines = data["components"]
        lines = []
        for bom_line in bom_lines:
            if level == 1:
                lines.append(
                    {
                        "bom_id": bom_line["bom_id"],
                        "name": bom_line["name"],
                        "type": bom_line["type"],
                        "quantity": bom_line["quantity"],
                        "quantity_available": bom_line["quantity_available"],
                        "quantity_on_hand": bom_line["quantity_on_hand"],
                        "producible_qty": bom_line.get("producible_qty", False),
                        "uom": bom_line["uom_name"],
                        "prod_cost": bom_line["prod_cost"],
                        "bom_cost": bom_line["bom_cost"],
                        "route_name": bom_line["route_name"],
                        "route_detail": bom_line["route_detail"],
                        "lead_time": bom_line["lead_time"],
                        "level": bom_line["level"],
                        "code": bom_line["code"],
                        "availability_state": bom_line["availability_state"],
                        "availability_display": bom_line["availability_display"],
                        "visible": True,
                    }
                )
        return lines
