from odoo import models
from odoo.tools.translate import _
from datetime import datetime

class FlattenedBomXlsx(models.AbstractModel):
    _name = "report.mrp_flattened_bom_xlsx.flattened_bom_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Flattened BOM XLSX"

    def get_text_color(self, hex_color):
        """Determine if text should be black or white based on background color luminance.
        See https://www.w3.org/TR/WCAG21/#dfn-relative-luminance"""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return "#000000"

        linear_rgb = []
        for i in range(0, 6, 2):
            value = int(hex_color[i : i + 2], 16) / 255.0
            linear_rgb.append(
                value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
                )
        luminance = (
            0.2126 * linear_rgb[0] + 0.7152 * linear_rgb[1] + 0.0722 * linear_rgb[2]
        )
        return "#FFFFFF" if luminance < 0.179 else "#000000"

    def print_flattened_bom_lines(self, bom, requirements, sheet, row):
        i = row
        sheet.write(i, 0, bom.product_tmpl_id.name or "")
        sheet.write(i, 1, bom.code or "")
        sheet.write(i, 2, bom.display_name or "")
        sheet.write(i, 3, bom.product_qty)
        sheet.write(i, 4, bom.product_uom_id.name or "")
        sheet.write(i, 5, bom.code or "")
        i += 1
        for product, total_qty in requirements.items():
            sheet.write(i, 1, product.default_code or "")
            sheet.write(i, 2, product.display_name or "")
            sheet.write(i, 3, total_qty or 0.0)
            sheet.write(i, 4, product.uom_id.name or "")
            sheet.write(i, 5, product.code or "")
            i += 1
        return i

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties(
            {"comments": "Created with Python and XlsxWriter from Odoo"}
        )

        for bom in objects:
            export_date = datetime.now()
            bg_color = bom.company_id.secondary_color or "#FFFFCC"
            text_color = self.get_text_color(bg_color)

            title_style = workbook.add_format(
                {
                    "bold": True,
                    "bg_color": bg_color,
                    "font_color": text_color,
                    "bottom": 1,
                }
            )

            sheet_name = f"{bom.id}/{bom.code}"[:31]
            sheet = workbook.add_worksheet(sheet_name[:31])
            sheet.set_landscape()
            sheet.fit_to_pages(1, 0)
            sheet.set_zoom(100)
            sheet.set_column(0, 0, 40)
            sheet.set_column(1, 5, 20)
            sheet.set_column(3, 4, 10)

            # Company Info
            company_name = (
                bom.company_id.partner_id.contact_address_inline
                or bom.company_id.name
                or ""
            )
            header_text = f"© {company_name}"

            sheet.write(0, 0, header_text)
            sheet.write(0, 4, str(export_date))

            # Table Headers
            sheet_title = [
                _("BOM Name"),
                _("Product Reference"),
                _("Product Name"),
                _("Quantity"),
                _("Unit of Measure"),
                _("Reference"),
            ]
            sheet.write_row(1, 0, sheet_title, title_style)
            sheet.freeze_panes(2, 0)

            # Populate BoM Data
            i = 2
            starting_factor = bom.product_uom_id._compute_quantity(
                bom.product_qty, bom.product_tmpl_id.uom_id, round=False
            )
            totals = bom._get_flattened_totals(factor=starting_factor)
            self.print_flattened_bom_lines(bom, totals, sheet, i)
