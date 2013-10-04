# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2013 Serpent Consulting Services (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

from openerp import pooler
import time
from string import digits
import barcode
from osv.orm import browse_record
import tempfile
from openerp.report import report_sxw

class workcenter_code(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(workcenter_code, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'generate_barcode': self.generate_barcode,
        })
        
    def generate_barcode(self, barcode_string):
        temp_path_svg = tempfile.gettempdir()+"/temp_barcode_"+barcode_string+""
        code39 = barcode.get_barcode_class('code39')
        c39 = code39(str(barcode_string))
        c39.save(temp_path_svg)
        return temp_path_svg+".svg"
    
    
report_sxw.report_sxw('report.mrp.wc.barcode.webkit', 'mrp.workcenter', 'addons/mrp_operations_webkit/report/mrp_wc_barcode.mako',parser=workcenter_code,header=False)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
