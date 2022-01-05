# Copyright 2018-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestMRPBomCurrentStock(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestMRPBomCurrentStock, cls).setUpClass()

        cls.product_obj = cls.env["product.product"]
        cls.bom_obj = cls.env["mrp.bom"]
        cls.bom_line_obj = cls.env["mrp.bom.line"]

        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")
        cls.uom_meter = cls.env.ref("uom.product_uom_meter")
        cls.uom_kgm = cls.env.ref("uom.product_uom_kgm")
        cls.uom_gm = cls.env.ref("uom.product_uom_gram")

        cls.stock_loc = cls.env.ref("stock.stock_location_stock")

        # Create products:
        cls.product_top = cls.product_obj.create(
            {
                "name": "FP-01",
                "type": "product",
                "uom_id": cls.uom_dozen.id,
                "uom_po_id": cls.uom_dozen.id,
            }
        )
        cls.product_sub_1 = cls.product_obj.create(
            {
                "name": "IP-01",
                "type": "product",
                "uom_id": cls.uom_dozen.id,
                "uom_po_id": cls.uom_dozen.id,
            }
        )
        cls.product_sub_2 = cls.product_obj.create(
            {
                "name": "IP-02",
                "type": "product",
                "uom_id": cls.uom_kgm.id,
                "uom_po_id": cls.uom_kgm.id,
            }
        )
        cls.product_sub_3 = cls.product_obj.create(
            {
                "name": "IP-03",
                "type": "product",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
            }
        )

        cls.component_1 = cls.product_obj.create(
            {
                "name": "PP-01",
                "type": "product",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
            }
        )
        cls.component_2 = cls.product_obj.create(
            {
                "name": "PP-02",
                "type": "product",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
            }
        )
        cls.component_3 = cls.product_obj.create(
            {
                "name": "PP-03",
                "type": "product",
                "uom_id": cls.uom_meter.id,
                "uom_po_id": cls.uom_meter.id,
            }
        )

        # Create Bills of Materials:
        cls.bom_top = cls.bom_obj.create(
            {
                "product_tmpl_id": cls.product_top.product_tmpl_id.id,
                "product_qty": 1.0,
                "product_uom_id": cls.uom_unit.id,
            }
        )
        cls.line_top_1 = cls.bom_line_obj.create(
            {
                "product_id": cls.product_sub_1.id,
                "bom_id": cls.bom_top.id,
                "product_qty": 1.0,
                "product_uom_id": cls.uom_dozen.id,
            }
        )
        cls.line_top_2 = cls.bom_line_obj.create(
            {
                "product_id": cls.product_sub_2.id,
                "bom_id": cls.bom_top.id,
                "product_qty": 200.0,
                "product_uom_id": cls.uom_gm.id,
            }
        )
        cls.line_top_3 = cls.bom_line_obj.create(
            {
                "product_id": cls.product_sub_3.id,
                "bom_id": cls.bom_top.id,
                "product_qty": 1.0,
                "product_uom_id": cls.uom_dozen.id,
            }
        )

        cls.bom_sub_1 = cls.bom_obj.create(
            {
                "product_tmpl_id": cls.product_sub_1.product_tmpl_id.id,
                "product_qty": 12.0,
                "product_uom_id": cls.uom_unit.id,
            }
        )
        cls.line_sub_1_1 = cls.bom_line_obj.create(
            {
                "product_id": cls.component_1.id,
                "bom_id": cls.bom_sub_1.id,
                "product_qty": 1.0,
                "product_uom_id": cls.uom_dozen.id,
            }
        )

        cls.bom_sub_2 = cls.bom_obj.create(
            {
                "product_tmpl_id": cls.product_sub_2.product_tmpl_id.id,
                "product_qty": 20.0,
                "product_uom_id": cls.uom_kgm.id,
            }
        )
        cls.line_sub_2_1 = cls.bom_line_obj.create(
            {
                "product_id": cls.component_2.id,
                "bom_id": cls.bom_sub_2.id,
                "product_qty": 1.0,
                "product_uom_id": cls.uom_unit.id,
            }
        )

        cls.bom_sub_3 = cls.bom_obj.create(
            {
                "product_tmpl_id": cls.product_sub_3.product_tmpl_id.id,
                "product_qty": 10.0,
                "product_uom_id": cls.uom_unit.id,
            }
        )
        cls.line_sub_3_1 = cls.bom_line_obj.create(
            {
                "product_id": cls.component_3.id,
                "bom_id": cls.bom_sub_3.id,
                "product_qty": 2.0,
                "product_uom_id": cls.uom_meter.id,
            }
        )

    def _product_change_qty(self, product, new_qty):
        values = {
            "product_id": product.id,
            "new_quantity": new_qty,
            "product_tmpl_id": product.product_tmpl_id.id,
        }
        wizard = self.env["stock.change.product.qty"].create(values)
        wizard.change_product_qty()

    def test_wizard(self):
        self.wizard = self.env["mrp.bom.current.stock"].create(
            {
                "product_id": self.product_top.id,
                "bom_id": self.bom_top.id,
                "location_id": self.stock_loc.id,
            }
        )
        self.wizard.do_explode()
        sol = (1, 1, 200, 0.01, 1, 2.4)
        lines = self.wizard.line_ids
        self.assertEquals(self.wizard.location_id, self.stock_loc)
        for i, line in enumerate(lines):
            self.assertEqual(line.product_qty, sol[i])
            self._product_change_qty(line.product_id, line.product_qty)
        lines._compute_qty_available_in_source_loc()
        for line in lines:
            available = line.product_id.product_tmpl_id.uom_id._compute_quantity(
                line.product_qty, line.product_uom_id
            )
            self.assertEqual(line.qty_available_in_source_loc, available)
