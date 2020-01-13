# © Copyright 2017-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class MRPBomStructureReportLevel1(models.AbstractModel):
    _name = "report.mrp_bom_structure_report_level_1.mrp_bs_l1"
    _inherit = "report.mrp.report_bom_structure"
    _description = "BOM Structure Report Level 1"

    def _get_pdf_line(
        self, bom_id, product_id=False, qty=1, child_bom_ids=None, unfolded=False
    ):

        if child_bom_ids is None:
            child_bom_ids = []

        data = self._get_bom(bom_id=bom_id, product_id=product_id.id, line_qty=qty)

        def get_sub_lines(bom, product_id, line_qty, line_id, level):
            data = self._get_bom(
                bom_id=bom.id,
                product_id=product_id.id,
                line_qty=line_qty,
                line_id=line_id,
                level=level,
            )
            bom_lines = data["components"]
            lines = []
            for bom_line in bom_lines:
                lines.append(
                    {
                        "name": bom_line["prod_name"],
                        "type": "bom",
                        "quantity": bom_line["prod_qty"],
                        "uom": bom_line["prod_uom"],
                        "prod_cost": bom_line["prod_cost"],
                        "bom_cost": bom_line["total"],
                        "level": bom_line["level"],
                        "code": bom_line["code"],
                    }
                )
            if data["operations"]:
                lines.append(
                    {
                        "name": _("Operations"),
                        "type": "operation",
                        "quantity": data["operations_time"],
                        "uom": _("minutes"),
                        "bom_cost": data["operations_cost"],
                        "level": level,
                    }
                )
            return lines

        bom = self.env["mrp.bom"].browse(bom_id)
        product = product_id or bom.product_id or bom.product_tmpl_id.product_variant_id
        pdf_lines = get_sub_lines(bom, product, qty, False, 1)
        data["components"] = []
        data["lines"] = pdf_lines
        return data
