# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class ComponentReportXlsx(models.AbstractModel):
    _name = "report.mrp_comp_xlsx.component_report"
    _inherit = "report.report_xlsx.abstract"
    _description = "MRP Production Component XLSX Report"

    @staticmethod
    def _get_component_totals(orders):
        """Return dict {product_id: {'name': str, 'qty': float, 'uom': str}}"""
        totals = {}
        for mo in orders:
            for move in mo.move_raw_ids.filtered(
                lambda m: m.state not in ("draft", "cancel")
            ):
                prod = move.product_id
                qty = move.product_uom._compute_quantity(
                    move.product_uom_qty, prod.uom_id
                )
                if prod.id not in totals:
                    totals[prod.id] = {
                        "name": prod.display_name,
                        "qty": 0.0,
                        "uom": prod.uom_id.name,
                    }
                totals[prod.id]["qty"] += qty
        return totals

    # -------------------- XLSX generator --------------------
    def generate_xlsx_report(self, workbook, data, objects):  # pragma: no cover
        sheet = workbook.add_worksheet(_("Components"))
        bold = workbook.add_format({"bold": True})
        uom_header = workbook.add_format({"bold": True, "bg_color": "#C6EFCE"})
        uom_cell = workbook.add_format({"bg_color": "#C6EFCE"})

        # Headers
        headers = [_("Component Name"), _("Quantity"), _("UoM")]
        for col, title in enumerate(headers):
            fmt = bold if col < 2 else uom_header
            sheet.write(0, col, title, fmt)

        totals = self._get_component_totals(objects)

        # Write data
        row = 1
        for prod_id in sorted(totals, key=lambda x: totals[x]["name"].lower()):
            entry = totals[prod_id]
            sheet.write(row, 0, entry["name"])
            sheet.write(row, 1, entry["qty"])
            sheet.write(row, 2, entry["uom"], uom_cell)
            row += 1
