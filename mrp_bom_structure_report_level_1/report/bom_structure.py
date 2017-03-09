# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
#        (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv
from openerp.report import report_sxw


class bom_structure(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bom_structure, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_children': self.get_children,
        })

    def get_children(self, object, level=0):
        result = []

        def _get_rec(object, level):
            for l in object:
                res = {}
                res['pname'] = l.product_id.display_name
                res['pcode'] = l.product_id.default_code
                res['pqty'] = l.product_qty
                res['uname'] = l.product_uom.name
                res['level'] = level
                res['code'] = l.bom_id.code
                result.append(res)
            return result

        children = _get_rec(object, level)

        return children


class report_mrpbomstructure_l0(osv.AbstractModel):
    _name = 'report.mrp_bom_structure_report_level_1.report_mrp_bs_l1'
    _inherit = 'report.mrp.report_mrpbomstructure'
    _template = 'mrp_bom_structure_report_level_1.report_mrp_bs_l1'
    _wrapped_report_class = bom_structure
