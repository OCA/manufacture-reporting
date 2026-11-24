# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from io import BytesIO

from openpyxl import load_workbook

from odoo.addons.mrp_bom_structure_xlsx.tests.common import TestMrpBomStructureXlsxBase


class TestMrpBomStructureXlsxLevel1(TestMrpBomStructureXlsxBase):
    def test_bom_structure_xlsx_report(self):
        res = self.report_model._render(
            "mrp_bom_structure_xlsx_l1.bom_structure_xlsx_l1", self.bom.ids, False
        )
        wb = load_workbook(BytesIO(res[0]))
        sheet = wb.worksheets[0]
        references = [row[2] for row in sheet.iter_rows(min_row=3, values_only=True)]
        self.assertIn("COMPONENT-A", references)
        self.assertIn("COMPONENT-B", references)
        self.assertNotIn("CHILD-COMPONENT", references)
