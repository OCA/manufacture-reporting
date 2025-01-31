# Copyright 2018 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import io
import zipfile

from odoo.tests.common import TransactionCase


class TestFlattenedBom(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_obj = cls.env["product.product"]
        cls.bom_obj = cls.env["mrp.bom"]
        cls.bom_line_obj = cls.env["mrp.bom.line"]
        cls.report_obj = cls.env.ref("mrp_flattened_bom_xlsx.flattened_bom_xlsx")

        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")

        # Create products:
        cls.product_top = cls.product_obj.create(
            {"name": "Final Product", "type": "product", "standard_price": 300.0}
        )
        cls.product_sub_1 = cls.product_obj.create(
            {"name": "L01-01", "type": "product", "standard_price": 300.0}
        )
        cls.product_sub_2 = cls.product_obj.create(
            {"name": "L01-02", "type": "product", "standard_price": 300.0}
        )
        cls.component_1 = cls.product_obj.create(
            {"name": "RM 01", "type": "product", "standard_price": 100.0}
        )
        cls.component_2 = cls.product_obj.create(
            {"name": "RM 01", "type": "product", "standard_price": 75.0}
        )
        cls.component_3 = cls.product_obj.create(
            {"name": "RM 03", "type": "product", "standard_price": 75.0}
        )

        # Create Bills of Materials:
        cls.bom_top = cls.bom_obj.create(
            {"product_tmpl_id": cls.product_top.product_tmpl_id.id}
        )
        cls.line_top_1 = cls.bom_line_obj.create(
            {
                "product_id": cls.product_sub_1.id,
                "bom_id": cls.bom_top.id,
                "product_qty": 2.0,
            }
        )
        cls.line_top_2 = cls.bom_line_obj.create(
            {
                "product_id": cls.product_sub_2.id,
                "bom_id": cls.bom_top.id,
                "product_qty": 5.0,
            }
        )

        cls.bom_sub_1 = cls.bom_obj.create(
            {"product_tmpl_id": cls.product_sub_1.product_tmpl_id.id}
        )
        cls.line_sub_1_1 = cls.bom_line_obj.create(
            {
                "product_id": cls.component_1.id,
                "bom_id": cls.bom_sub_1.id,
                "product_qty": 2.0,
            }
        )
        cls.line_sub_1_2 = cls.bom_line_obj.create(
            {
                "product_id": cls.component_2.id,
                "bom_id": cls.bom_sub_1.id,
                "product_qty": 5.0,
            }
        )

        cls.bom_sub_2 = cls.bom_obj.create(
            {"product_tmpl_id": cls.product_sub_2.product_tmpl_id.id}
        )
        cls.line_sub_2_1 = cls.bom_line_obj.create(
            {
                "product_id": cls.component_1.id,
                "bom_id": cls.bom_sub_2.id,
                "product_qty": 3.0,
            }
        )
        cls.line_sub_2_2 = cls.bom_line_obj.create(
            {
                "product_id": cls.component_3.id,
                "bom_id": cls.bom_sub_2.id,
                "product_qty": 3.0,
            }
        )

    def test_01_flattened_totals(self):
        """Test totals computation with a multi level BoM."""
        flat_tot = self.bom_top._get_flattened_totals()
        self.assertEqual(len(flat_tot), 3)
        # Component 1 = 2*2 + 5*3 = 19
        self.assertEqual(flat_tot.get(self.component_1), 19)
        # Component 2 = 2*5 = 10
        self.assertEqual(flat_tot.get(self.component_2), 10)
        # Component 3 = 5*3 = 15
        self.assertEqual(flat_tot.get(self.component_3), 15)

    def test_02_different_uom(self):
        """Test totals computation with a multi level BoM and different UoM."""
        self.bom_top.product_uom_id = self.uom_dozen
        self.line_sub_2_1.product_uom_id = self.uom_dozen
        flat_tot = self.bom_top._get_flattened_totals()
        self.assertEqual(len(flat_tot), 3)
        # Component 1 = 2*2 + 5*3*12 = 184 units -> 184/12 dozens
        self.assertAlmostEqual(flat_tot.get(self.component_1), 184 / 12)
        # Component 2 = 2*5 = 10 units -> 10/12 dozens
        self.assertAlmostEqual(flat_tot.get(self.component_2), 10 / 12)
        # Component 3 = 5*3 = 15 units -> 15/12 dozens
        self.assertAlmostEqual(flat_tot.get(self.component_3), 15 / 12)

    def test_03_multiple_export(self):
        """Test XLSX report generation with separate sheets for each BoM selected"""
        report = self.report_obj
        bom_records = self.bom_top | self.bom_sub_1 | self.bom_sub_2

        # Generate the report
        report_data = report._render_xlsx(
            "mrp_flattened_bom_xlsx.flattened_bom_xlsx", bom_records.ids, data={}
        )
        report_bytes = report_data[0]

        with zipfile.ZipFile(io.BytesIO(report_bytes), "r") as xlsx_zip:
            sheet_files = [
                name
                for name in xlsx_zip.namelist()
                if name.startswith("xl/worksheets/sheet")
            ]

        # Ensure the correct number of sheets exists
        self.assertEqual(len(bom_records), len(sheet_files))

    def test_get_text_color(self):
        """Test that text color is correctly determined based on background luminance."""

        # {background_color: expected_text_color}
        test_cases = {
            "#FFFFFF": "#000000",  # White background -> Black text
            "#000000": "#FFFFFF",  # Black background -> White text
            "#FF0000": "#000000",  # Red background -> Black text
            "#00FF00": "#000000",  # Green background -> Black text
            "#0000FF": "#FFFFFF",  # Blue background -> White text
            "#FFFF00": "#000000",  # Yellow background -> Black text
            "#00FFFF": "#000000",  # Cyan background -> Black text
            "#FF00FF": "#000000",  # Magenta background -> Black text
            "#808080": "#000000",  # Gray background -> Black text
            "#C0C0C0": "#000000",  # Light gray -> Black text
            "#101010": "#FFFFFF",  # Dark gray -> White text
        }

        model_instance = self.env["report.mrp_flattened_bom_xlsx.flattened_bom_xlsx"]
        for bg_color, expected_text_color in test_cases.items():
            with self.subTest(bg_color=bg_color):
                result = model_instance.get_text_color(bg_color)

                self.assertEqual(result, expected_text_color, f"Failed for {bg_color}")
