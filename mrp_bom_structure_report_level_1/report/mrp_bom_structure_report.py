# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
#        (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.osv import osv
from odoo.report import report_sxw


class BomStructureReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(BomStructureReport, self).__init__(cr, uid, name,
                                                 context=context)
        self.localcontext.update({
            'get_children': self.get_children,
        })

    def get_children(self, object, level=0):
        result = []

        def _get_rec(object, level, qty=1.0, uom=False):
            for l in object:
                res = {}
                res['pname'] = l.product_id.name_get()[0][1]
                res['pcode'] = l.product_id.default_code
                qty_per_bom = l.bom_id.product_qty
                if uom:
                    if uom != l.bom_id.product_uom_id:
                        qty = uom._compute_quantity(qty,
                                                    l.bom_id.product_uom_id)
                    res['pqty'] = (l.product_qty * qty) / qty_per_bom
                else:
                    # for the first case, the ponderation is right
                    res['pqty'] = (l.product_qty * qty)
                res['puom'] = l.product_uom_id
                res['uname'] = l.product_uom_id.name
                res['level'] = level
                res['code'] = l.bom_id.code
                result.append(res)
            return result

        children = _get_rec(object, level)

        return children


class ReportMrpbomStructureL0(osv.AbstractModel):
    _name = 'report.mrp_bom_structure_report_level_1.report_mrp_bs_l1'
    _inherit = 'report.mrp.report_mrpbomstructure'
    _template = 'mrp_bom_structure_report_level_1.report_mrp_bs_l1'
    _wrapped_report_class = BomStructureReport
