# © 2017 Eficent Business and IT Consulting Services S.L.
#        (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.mrp.report.mrp_bom_structure_report import BomStructureReport


class BomStructureReportLevel1(BomStructureReport):
    _name = 'report.mrp_bom_structure_report_level_1.mrp_bs_l1'

    def get_children(self, records, level=0):
        result = []

        def _get_rec(records, level, qty=1.0, uom=False):
            for l in records:
                child = self._get_child_vals(l, level, qty, uom)
                result.append(child)
            return result

        children = _get_rec(records, level)

        return children
