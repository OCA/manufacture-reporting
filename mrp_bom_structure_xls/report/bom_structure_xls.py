# -*- coding: utf-8 -*-
# Copyright 2016-2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import xlwt
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.mrp.report.bom_structure \
    import bom_structure
from openerp.tools.translate import _


class BomStructureXls(report_xls):
    column_sizes = [40, 20, 20, 40, 20, 20, 20]

    def global_initializations(self, wb, _p, xlwtlib, _xs, objects, data):
        # this procedure will initialise variables and Excel cell styles and
        # return them as global ones
        self.ws = wb.add_sheet(_('BOM Structure'))
        self.ws.panes_frozen = True
        self.ws.remove_splits = True
        self.ws.portrait = 0  # Landscape
        self.ws.fit_width_to_pages = 1
        self.ws.header_str = self.xls_headers['standard']
        self.ws.footer_str = self.xls_footers['standard']
        # -------------------------------------------------------
        # number of columns
        self.nbr_columns = 7
        # -------------------------------------------------------
        self.style_default = xlwtlib.easyxf(_xs['borders_all'])
        # -------------------------------------------------------
        self.style_bold = xlwtlib.easyxf(_xs['bold'] + _xs['borders_all'])
        # -------------------------------------------------------
        # cell style for columns titles
        self.style_yellow_bold = xlwtlib.easyxf(
            _xs['bold'] + _xs['fill'] + _xs['borders_all'])
        # -------------------------------------------------------

    # send an empty row to the Excel document
    def print_empty_row(self, row_position):
        c_sizes = self.column_sizes
        c_specs = [('empty%s' % i, 1, c_sizes[i], 'text', None)
                   for i in range(0, len(c_sizes))]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            self.ws, row_position, row_data, set_column_size=True)
        return row_position

    # Fill in a row with the titles of the columns
    def print_columns_title(self, _p, data, row_position):
        c_specs = [
            ('bom_name_title', 1, 0, 'text', _('BOM Name'), None,
             self.style_yellow_bold),
            ('level_title', 1, 0, 'text', _('Level'),
             None, self.style_yellow_bold),
            ('product_code_title', 1, 0, 'text', _('Product Reference'),
             None, self.style_yellow_bold),
            ('product_name_title', 1, 0, 'text', _('Product Name'),
             None, self.style_yellow_bold),
            ('quantity_title', 1, 0, 'text', _('Quantity'), None,
             self.style_yellow_bold),
            ('uom_title', 1, 0, 'text', _('Unit of Measure'), None,
             self.style_yellow_bold),
            ('bom_ref_title', 1, 0, 'text', _('Reference'),
             None, self.style_yellow_bold),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            self.ws, row_position, row_data, row_style=self.style_yellow_bold)
        return row_position

    # export the BOMs
    def print_boms(self, row_position, bom, _xs, xlwtlib, _p, data):
        c_specs = [
            ('bom_name', 1, 0, 'text', bom.name or ''),
            ('level', 1, 0, 'text', ''),
            ('product_code', 1, 0, 'text', bom.product_id.default_code or ''),
            ('product_name', 1, 0, 'text', bom.product_id.name or ''),
            ('quantity', 1, 0, 'number', bom.product_qty),
            ('uom', 1, 0, 'text', bom.product_uom.name or ''),
            ('bom_ref', 1, 0, 'text', bom.code or ''),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            self.ws, row_position, row_data, self.style_bold)
        return row_position

    # export the BOM children
    def print_bom_children(self, row_position, ch, _xs, xlwtlib, _p, data):
        bom_level = '> '*(ch.get('level', 0)+1)
        code = ch.get('code') or ''
        c_specs = [
            ('bom_name_child', 1, 0, 'text', ch.get('name', '')),
            ('level', 1, 0, 'text', bom_level),
            ('product_code_child', 1, 0, 'text', ch.get('pcode', '')),
            ('product_name_child', 1, 0, 'text', ch.get('pname', '')),
            ('quantity_child', 1, 0, 'number', ch.get('pqty', '')),
            ('uom_child', 1, 0, 'text', ch.get('uname', '')),
            ('bom_ref_child', 1, 0, 'text', code),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            self.ws, row_position, row_data, row_style=self.style_default)
        return row_position

    def generate_xls_report(self, _p, _xs, data, objects, wb):  # main function

        # Initializations
        self.global_initializations(wb, _p, xlwt, _xs, objects, data)
        row_pos = 0
        # Print empty row to define column sizes
        row_pos = self.print_empty_row(row_pos)
        # Print Header Table data
        row_pos = self.print_columns_title(_p, data, row_pos)
        # Freeze the line
        self.ws.set_horz_split_pos(row_pos)
        for o in objects:
            # call xls
            row_pos = self.print_boms(row_pos, o, _xs, xlwt, _p, data)
            for ch in _p.get_children(o.bom_line_ids):
                row_pos = self.print_bom_children(row_pos, ch, _xs, xlwt,
                                                  _p, data)


BomStructureXls('report.bom.structure.xls', 'mrp.bom', parser=bom_structure)
