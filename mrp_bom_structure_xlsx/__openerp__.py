# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Export BOM Structure to Excel .XLSX",
    'version': '9.0.1.0.0',
    'category': 'Manufacturing',
    'author': "Eficent, Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/manufacture-reporting',
    'license': 'AGPL-3',
    "depends": ['report_xlsx', 'mrp'],
    "data": [
        'report/bom_structure_xlsx.xml',
    ],
    "installable": True
}
