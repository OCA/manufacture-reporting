from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_mrp_bom_fixed_quantity = fields.Boolean("Fixed Quantity")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            module_mrp_bom_fixed_quantity=self.env["ir.config_parameter"]
            .sudo()
            .get_param("mrp.module_mrp_bom_fixed_quantity")
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "mrp.module_mrp_bom_fixed_quantity",
            self.module_mrp_bom_fixed_quantity
        )
