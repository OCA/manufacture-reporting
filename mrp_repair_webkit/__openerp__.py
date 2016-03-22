# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#                             (<http://www.serpentcs.com>)
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

{
    'name': 'Repairs Management - Webkit Report',
    'version': '1.0',
    'category': 'Manufacturing',
    'description': """
Webkit report for mrp repair
=============================

The aim is to have a complete module to manage all products repairs.

It is conversion of rml report to Webkit Report.
""",
    "license": "AGPL-3",
    'author': "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    'website': 'http://www.serpentcs.com',
    'depends': ['report_webkit', 'mrp_repair'],
    'data': ['mrp_repair_report.xml'],
    'images': [],
    'installable': True,
    'auto_install': False,
}
