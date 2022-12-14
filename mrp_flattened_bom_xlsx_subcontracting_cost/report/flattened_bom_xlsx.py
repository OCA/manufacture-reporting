# Copyright 2022 ForgeFlow S.L. (http://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from collections import OrderedDict

from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class FlattenedBomXlsx(models.AbstractModel):
    _inherit = "report.mrp_flattened_bom_xlsx.flattened_bom_xlsx"

    def _get_bom_subcontracting_values(self, o, bom, qty):
        return [
            o.product_tmpl_id.name or "",
            bom.product_tmpl_id.name or "",
            bom.product_tmpl_id.default_code or "",
            bom.display_name or "",
            bom.subcontractor_ids[0].name or "",
            qty,
            bom.product_tmpl_id.uom_id.name or "",
            bom.subcontracting_cost or 0.0,
            bom.subcontracting_cost * qty or 0.0,
            bom.product_tmpl_id.currency_id.symbol or "",
        ]

    def _print_bom_line_subcontracted(self, o, bom, llc, qty, sheet, row, n_columns):
        sheet.write(row, 0, llc)
        values = self._get_bom_subcontracting_values(o, bom, qty)
        for j in range(1, n_columns):
            sheet.write(row, j, values[j - 1])
        row += 1
        return row

    def _get_bom_structure_dict(self, boms, bom, llc, qty):
        """
        Return BoM structure without last level of materials.
        :returns: dict: keys are BoM identifiers and values
        are [llc, qty] objects.
        """
        boms[bom.id] = [llc, qty]
        for line in bom.bom_line_ids:
            if line.product_id.bom_ids:
                boms = self._get_bom_structure_dict(
                    boms, line.product_id.bom_ids[0], llc + 1, qty * line.product_qty
                )
        return boms

    def _get_subcontracting_title_values(self):
        return [
            _("Level"),
            _("Main BOM"),
            _("Subcontracted BOM"),
            _("Internal Reference"),
            _("Product Name"),
            _("Partner Name"),
            _("Quantity"),
            _("Unit of Measure"),
            _("Subcontracting Unit Cost"),
            _("Subcontracting Cost"),
            _("Currency"),
        ]

    def _generate_xlsx_subcontracting_sheet_format(self, sheet):
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 3, 20)
        sheet.set_column(4, 4, 30)
        sheet.set_column(5, 10, 20)

    def generate_xlsx_report(self, workbook, data, objects):
        res = super().generate_xlsx_report(workbook, data, objects)
        sheet = workbook.add_worksheet(_("Subcontracting Costs"))

        self._generate_xlsx_subcontracting_sheet_format(sheet)
        title_style = workbook.add_format(
            {"bold": True, "bg_color": "#FFFFCC", "bottom": 1}
        )
        sheet_title = self._get_subcontracting_title_values()
        sheet.set_row(0, None, None, {"collapsed": 1})
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        n_columns = len(sheet_title)

        i = 2
        bom_model = self.env["mrp.bom"]
        for o in objects:
            boms = {}
            boms = self._get_bom_structure_dict(boms, o, 0, 1.0)
            for key in OrderedDict(sorted(boms.items(), key=lambda x: x[1][0])):
                bom = bom_model.browse(key)
                llc = boms[key][0]
                qty = boms[key][1]
                if bom.type == "subcontract" and bom.subcontractor_ids:
                    i = self._print_bom_line_subcontracted(
                        o, bom, llc, qty, sheet, i, n_columns
                    )
        return res
