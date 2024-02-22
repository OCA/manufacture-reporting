# Copyright 2018-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class ReportMrpBomCurrentStockXlsx(models.AbstractModel):
    _name = "report.mrp_bom_current_stock.report_mrpbom_current_stock_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "MRP BOM Current Stock XLSX Report"

    @staticmethod
    def _print_bom_children(ch, sheet, row):
        i = row
        sheet.write(i, 0, ch.bom_level or "")
        sheet.write(i, 1, ch.bom_line.bom_id.code or "")
        sheet.write(i, 2, ch.product_id.product_tmpl_id.display_name or "")
        sheet.write(i, 3, ch.product_qty or "")
        sheet.write(i, 4, ch.qty_available_in_source_loc or 0.0)
        sheet.write(i, 5, ch.product_uom_id.name or "")
        sheet.write(i, 6, ch.location_id.name or "")
        sheet.write(i, 7, ch.bom_id.code or "")
        sheet.write(i, 8, ch.bom_id.product_tmpl_id.display_name or "")
        i += 1
        return i

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties(
            {"comments": "Created with Python and XlsxWriter from Odoo 11.0"}
        )
        sheet = workbook.add_worksheet(_("BOM Current Stock Report"))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 2, 40)
        sheet.set_column(3, 3, 10)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 7)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 8, 40)

        title_style = workbook.add_format(
            {"bold": True, "bg_color": "#FFFFCC", "bottom": 1}
        )
        sheet_title = [
            _("Level"),
            _("BoM Reference"),
            _("Product Reference"),
            _("Quantity"),
            _("Qty Available (Location)"),
            _("UoM"),
            _("Location"),
            _("Parent BoM Ref"),
            _("Parent Product Ref"),
        ]
        sheet.set_row(0, None, None, {"collapsed": 1})
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        bold = workbook.add_format({"bold": True})

        i = 2
        for o in objects:
            sheet.write(i, 0, "0", bold)
            sheet.write(i, 1, o.bom_id.code or "", bold)
            sheet.write(i, 2, o.product_tmpl_id.name or "", bold)

            sheet.write(i, 3, o.product_qty or "", bold)
            sheet.write(i, 5, o.product_uom_id.name or "", bold)
            sheet.write(i, 6, o.location_id.name or "", bold)
            i += 1
            for ch in o.line_ids:
                i = self._print_bom_children(ch, sheet, i)
