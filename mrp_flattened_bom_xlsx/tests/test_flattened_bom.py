# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestFlattenedBom(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestFlattenedBom, cls).setUpClass()

        cls.product_obj = cls.env['product.product']
        cls.bom_obj = cls.env['mrp.bom']
        cls.bom_line_obj = cls.env['mrp.bom.line']

        cls.uom_dozen = cls.env.ref('product.product_uom_dozen')

        # Create products:
        cls.product_top = cls.product_obj.create({
            'name': 'Final Product',
            'type': 'product',
            'standard_price': 300.0,
        })
        cls.product_sub_1 = cls.product_obj.create({
            'name': 'L01-01',
            'type': 'product',
            'standard_price': 300.0,
        })
        cls.product_sub_2 = cls.product_obj.create({
            'name': 'L01-02',
            'type': 'product',
            'standard_price': 300.0,
        })
        cls.component_1 = cls.product_obj.create({
            'name': 'RM 01',
            'type': 'product',
            'standard_price': 100.0,
        })
        cls.component_2 = cls.product_obj.create({
            'name': 'RM 01',
            'type': 'product',
            'standard_price': 75.0,
        })
        cls.component_3 = cls.product_obj.create({
            'name': 'RM 03',
            'type': 'product',
            'standard_price': 75.0,
        })

        # Create Bills of Materials:
        cls.bom_top = cls.bom_obj.create({
            'product_tmpl_id': cls.product_top.product_tmpl_id.id,

        })
        cls.line_top_1 = cls.bom_line_obj.create({
            'product_id': cls.product_sub_1.id,
            'bom_id': cls.bom_top.id,
            'product_qty': 2.0,
        })
        cls.line_top_2 = cls.bom_line_obj.create({
            'product_id': cls.product_sub_2.id,
            'bom_id': cls.bom_top.id,
            'product_qty': 5.0,
        })

        cls.bom_sub_1 = cls.bom_obj.create({
            'product_tmpl_id': cls.product_sub_1.product_tmpl_id.id,

        })
        cls.line_sub_1_1 = cls.bom_line_obj.create({
            'product_id': cls.component_1.id,
            'bom_id': cls.bom_sub_1.id,
            'product_qty': 2.0,
        })
        cls.line_sub_1_2 = cls.bom_line_obj.create({
            'product_id': cls.component_2.id,
            'bom_id': cls.bom_sub_1.id,
            'product_qty': 5.0,
        })

        cls.bom_sub_2 = cls.bom_obj.create({
            'product_tmpl_id': cls.product_sub_2.product_tmpl_id.id,

        })
        cls.line_sub_2_1 = cls.bom_line_obj.create({
            'product_id': cls.component_1.id,
            'bom_id': cls.bom_sub_2.id,
            'product_qty': 3.0,
        })
        cls.line_sub_2_2 = cls.bom_line_obj.create({
            'product_id': cls.component_3.id,
            'bom_id': cls.bom_sub_2.id,
            'product_qty': 3.0,
        })

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
