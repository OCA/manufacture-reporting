# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from xlrd import open_workbook

from odoo.addons.mrp_bom_structure_xlsx.tests.common import TestMrpBomStructureXlsxBase


class TestMrpBomStructureXlsxLevel1(TestMrpBomStructureXlsxBase):
    def test_bom_structure_xlsx_report(self):
        res = self.report_model._render(
            "mrp_bom_structure_xlsx_l1.bom_structure_xlsx_l1", self.bom.ids, False
        )
        wb = open_workbook(file_contents=res[0])
        sheet = wb.sheet_by_index(0)
        references = [sheet.cell_value(row, 2) for row in range(2, sheet.nrows)]
        self.assertIn("COMPONENT-A", references)
        self.assertIn("COMPONENT-B", references)
        self.assertNotIn("CHILD-COMPONENT", references)
