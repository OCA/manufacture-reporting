# -*- coding: utf-8 -*-
# Copyright 2016-2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo.report import report_sxw
from odoo.addons.mrp_bom_structure_xlsx.report.bom_structure_xlsx import \
    BomStructureXlsx

_logger = logging.getLogger(__name__)

try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    _logger.debug("report_xlsx not installed, Excel export non functional")

    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass


class BomStructureXlsxL1(BomStructureXlsx):

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


BomStructureXlsxL1('report.bom.structure.xlsx.l1', 'mrp.bom',
                   parser=report_sxw.rml_parse)
