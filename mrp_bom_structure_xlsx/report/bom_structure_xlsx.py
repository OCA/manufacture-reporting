# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from odoo.report import report_sxw
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    _logger.debug("report_xlsx not installed, Excel export non functional")

    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass


class BomStructureXlsx(ReportXlsx):

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
        for child in ch.child_line_ids:
            i = self.print_bom_children(child, sheet, i, j)
        j -= 1
        return i

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 9.0'})
        sheet = workbook.add_worksheet(_('BOM Structure'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 2, 20)
        sheet.set_column(3, 3, 40)
        sheet.set_column(4, 6, 20)
        bold = workbook.add_format({'bold': True})
        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})
        sheet_title = [_('BOM Name'),
                       _('Level'),
                       _('Product Reference'),
                       _('Product Name'),
                       _('Quantity'),
                       _('Unit of Measure'),
                       _('Reference')
                       ]
        sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        i = 2
        for o in objects:
            sheet.write(i, 0, o.product_tmpl_id.name or '', bold)
            sheet.write(i, 1, '', bold)
            sheet.write(i, 2, o.product_id.default_code or '', bold)
            sheet.write(i, 3, o.product_id.name or '', bold)
            sheet.write(i, 4, o.product_qty, bold)
            sheet.write(i, 5, o.product_uom_id.name or '', bold)
            sheet.write(i, 6, o.code or '', bold)
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_bom_children(ch, sheet, i, j)


BomStructureXlsx('report.bom.structure.xlsx', 'mrp.bom',
                 parser=report_sxw.rml_parse)
