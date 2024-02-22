# Copyright 2022 ForgeFlow S.L. (http://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from collections import OrderedDict

from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class FlattenedBomXlsx(models.AbstractModel):
    _inherit = "report.mrp_flattened_bom_xlsx.flattened_bom_xlsx"

    def _get_bom_operation_values(self, bom, operation, qty):
        labour_cost = operation.workcenter_id.costs_hour * (operation.time_cycle / 60.0)
        return [
            bom.product_tmpl_id.name or "",
            bom.product_tmpl_id.default_code or "",
            bom.display_name or "",
            operation.name or "",
            operation.workcenter_id.name or "",
            qty,
            bom.product_tmpl_id.uom_id.name or "",
            operation.time_cycle / 60.0 or 0.0,
            operation.workcenter_id.costs_hour or 0.0,
            labour_cost or 0.0,
            labour_cost * qty or 0.0,
            bom.product_tmpl_id.currency_id.symbol or "",
        ]

    def _print_bom_lines_labour(self, bom, llc, qty, sheet, row, n_columns):
        for operation in bom.operation_ids:
            sheet.write(row, 0, llc)
            values = self._get_bom_operation_values(bom, operation, qty)
            for j in range(2, n_columns):
                sheet.write(row, j, values[j - 2])
            if llc == 0:
                sheet.write(row, 1, bom.product_tmpl_id.name or "")
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

    def _get_labour_title_values(self):
        return [
            _("Level"),
            _("Main BOM"),
            _("Sub BOMs"),
            _("Internal Reference"),
            _("Product Name"),
            _("Operation"),
            _("Work Center"),
            _("Quantity"),
            _("Unit of Measure"),
            _("Duration (hours)"),
            _("Cost per hour"),
            _("Labour Unit Cost"),
            _("Labour Cost"),
            _("Currency"),
        ]

    def _generate_xlsx_labour_sheet_format(self, sheet):
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 6, 20)
        sheet.set_column(7, 13, 15)

    def generate_xlsx_report(self, workbook, data, objects):
        res = super().generate_xlsx_report(workbook, data, objects)
        sheet = workbook.add_worksheet(_("Labour Costs"))

        self._generate_xlsx_labour_sheet_format(sheet)
        title_style = workbook.add_format(
            {"bold": True, "bg_color": "#FFFFCC", "bottom": 1}
        )
        sheet_title = self._get_labour_title_values()
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
                i = self._print_bom_lines_labour(bom, llc, qty, sheet, i, n_columns)

        return res
