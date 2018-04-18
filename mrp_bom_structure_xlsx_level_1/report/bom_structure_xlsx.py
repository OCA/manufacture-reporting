# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo.addons.mrp_bom_structure_xlsx.report.bom_structure_xlsx import \
    BomStructureXlsx

_logger = logging.getLogger(__name__)


class BomStructureXlsxL1(BomStructureXlsx):
    _name = 'report.mrp_bom_structure_xlsx_l1.bom_structure_xlsx_l1'

    def print_bom_children(self, ch, sheet, row, level):
        i, j = row, level
        j += 1
        sheet.write(i, 1, '> '*j)
        sheet.write(i, 2, ch.product_id.default_code or '')
        sheet.write(i, 3, ch.product_id.display_name or '')
        sheet.write(i, 4, ch.product_qty)
        sheet.write(i, 5, ch.product_uom_id.name or '')
        sheet.write(i, 6, ch.bom_id.code or '')
        i += 1
        return i
