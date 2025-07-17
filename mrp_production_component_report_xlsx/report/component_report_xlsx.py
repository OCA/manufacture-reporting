from collections import defaultdict

from odoo import _, models


class ComponentReportXlsx(models.AbstractModel):
    _name = "report.mrp_comp_xlsx.component_report"
    _inherit = "report.report_xlsx.abstract"
    _description = "MRP Production Component XLSX Report"

    def generate_xlsx_report(self, workbook, data, objects):
        sheet = workbook.add_worksheet(_("Components"))
        bold = workbook.add_format({"bold": True})
        # Headers
        headers = [_("Component Name"), _("Quantity")]
        for col, title in enumerate(headers):
            sheet.write(0, col, title, bold)
        # Aggregation
        comp = defaultdict(lambda: {"qty": 0.0, "name": ""})
        for mo in objects:
            for move in mo.move_raw_ids:
                prod = move.product_id
                qty = prod.uom_id._compute_quantity(move.product_uom_qty, prod.uom_id)
                rec = comp[prod.id]
                rec["qty"] += qty
                rec["name"] = prod.display_name
        # Record of data
        row = 1
        for pid in sorted(comp, key=lambda x: comp[x]["name"].lower()):
            r = comp[pid]
            sheet.write(row, 0, r["name"])
            sheet.write(row, 1, r["qty"])
            row += 1
