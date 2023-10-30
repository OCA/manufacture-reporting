# Copyright 2023 ForgeFlow S.L. (http://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_direct_material_unit_cost(self):
        self.ensure_one()
        if not self.standard_price and self.variant_seller_ids:
            return self.variant_seller_ids[0].price
        return self.standard_price
