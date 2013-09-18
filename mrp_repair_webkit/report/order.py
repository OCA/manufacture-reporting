# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.(<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import time
from openerp.report import report_sxw

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'total': self.total,
        })

    def total(self, repair):
        print "repair",repair
        total = 0.0
        for operation in repair.operations:
           total += operation.price_subtotal
        for fee in repair.fees_lines:
           total += fee.price_subtotal
        total = total + repair.amount_tax
        return total

report_sxw.report_sxw('report.repair.order.webkit','mrp.repair','addons/mrp_repair_webkit/report/order.mako',parser=order)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

