from odoo import exceptions
from odoo.addons.mrp.tests.common import TestMrpCommon


class TestMrpBom(TestMrpCommon):
    def test_explode_fixed(self):
        """ Test functionality of fixed quantity feature added to bom.

        structure EX boms:
        [(mrp.bom(16,),
        {'qty': 3, 'product': product.product(105,),
        'original_qty': 3, 'parent_line': False})]

        structure EX lines
        [
            (mrp.bom.line(40,),
            {'qty': 6.0, 'product': product.product(105,),
            'original_qty': 3, 'parent_line': False}),

            (mrp.bom.line(41,),
            {'qty': 12.0, 'product': product.product(105,),
            'original_qty': 3, 'parent_line': False})
        ]
        """
        # call explode on a bom object
        boms, lines = self.bom_1.explode(self.product_4, 5)
        # set the first item in the bom_line_ids bom, fixed_qty field to True
        lines[0][0].fixed_quantity = True
        # call explode again to test functionality of fixed quantity = True
        boms, lines = self.bom_1.explode(self.product_4, 10)
        # check if the dictionaries values for qty and original_qty =
        # the bom line's first object.product_qty after explode.
        self.assertEqual(lines[0][1]["qty"], lines[0][0].product_qty)
        self.assertEqual(lines[0][1]["original_qty"], lines[0][0].product_qty)
