# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestComponentReport(TransactionCase):
    """Verify aggregation helper _get_component_totals including UoM."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # store UoMs for later checks
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")

        # Components with different UoMs
        cls.comp_a = cls.env["product.product"].create(
            {
                "name": "A Comp",
                "uom_id": cls.uom_unit.id,
            }
        )
        cls.comp_b = cls.env["product.product"].create(
            {
                "name": "B Comp",
                "uom_id": cls.uom_dozen.id,
            }
        )

        # Finished product
        cls.finished = cls.env["product.product"].create(
            {
                "name": "Finished",
                "uom_id": cls.uom_unit.id,
            }
        )

        # BoM: 1×A + 1×B
        bom = cls.env["mrp.bom"].create(
            {"product_tmpl_id": cls.finished.product_tmpl_id.id}
        )
        cls.env["mrp.bom.line"].create(
            {"bom_id": bom.id, "product_id": cls.comp_a.id, "product_qty": 1}
        )
        cls.env["mrp.bom.line"].create(
            {
                "bom_id": bom.id,
                "product_id": cls.comp_b.id,
                "product_qty": 1,
                "product_uom_id": cls.uom_dozen.id,
            }
        )

        # Two MOs: 2 and 3 units
        cls.mo1 = cls.env["mrp.production"].create(
            {
                "product_id": cls.finished.id,
                "product_qty": 2,
                "product_uom_id": cls.uom_unit.id,
            }
        )
        cls.mo2 = cls.env["mrp.production"].create(
            {
                "product_id": cls.finished.id,
                "product_qty": 3,
                "product_uom_id": cls.uom_unit.id,
            }
        )
        (cls.mo1 + cls.mo2).action_confirm()

        cls.report = cls.env["report.mrp_comp_xlsx.component_report"]

    def test_multiple_mos_aggregation(self):
        """Components summed correctly with UoM labels."""
        totals = self.report._get_component_totals([self.mo1, self.mo2])
        self.assertEqual(totals[self.comp_a.id]["qty"], 5)  # 2+3
        self.assertEqual(totals[self.comp_b.id]["qty"], 5)
        # check UoM values
        self.assertEqual(totals[self.comp_a.id]["uom"], self.uom_unit.name)
        self.assertEqual(totals[self.comp_b.id]["uom"], self.uom_dozen.name)

    def test_empty_orders(self):
        """Empty list returns empty dict."""
        self.assertEqual(self.report._get_component_totals([]), {})

    def test_uom_conversion(self):
        """Quantities and UoM labels on single MO."""
        totals = self.report._get_component_totals([self.mo1])
        self.assertEqual(totals[self.comp_a.id]["qty"], 2)
        self.assertEqual(totals[self.comp_b.id]["qty"], 2)
        self.assertEqual(totals[self.comp_a.id]["uom"], self.uom_unit.name)
        self.assertEqual(totals[self.comp_b.id]["uom"], self.uom_dozen.name)
