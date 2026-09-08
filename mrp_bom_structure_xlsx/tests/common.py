# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestMrpBomStructureXlsxBase(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Test product", "default_code": "product"}
        )
        cls.component_a = cls.env["product.product"].create(
            {
                "name": "Test componente A",
                "default_code": "COMPONENT-A",
            }
        )
        cls.component_b = cls.env["product.product"].create(
            {
                "name": "Test componente B",
                "default_code": "COMPONENT-B",
            }
        )
        cls.report_model = cls.env["ir.actions.report"]
        # Bom from product
        bom_form = Form(cls.env["mrp.bom"])
        bom_form.product_tmpl_id = cls.product.product_tmpl_id
        with bom_form.bom_line_ids.new() as line_form:
            line_form.product_id = cls.component_a
            line_form.product_qty = 1
        with bom_form.bom_line_ids.new() as line_form:
            line_form.product_id = cls.component_b
            line_form.product_qty = 1
        cls.bom = bom_form.save()
        # Bom from component A
        cls.child_component = cls.env["product.product"].create(
            {
                "name": "Test child component",
                "default_code": "CHILD-COMPONENT",
            }
        )
        bom_form = Form(cls.env["mrp.bom"])
        bom_form.product_tmpl_id = cls.component_a.product_tmpl_id
        with bom_form.bom_line_ids.new() as line_form:
            line_form.product_id = cls.child_component
            line_form.product_qty = 1
        bom_form.save()
