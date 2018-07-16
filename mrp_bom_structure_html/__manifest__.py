# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Preview BOM Structure to HTML",
    'version': '11.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Preview Bill of Materials Structure',
    'author': "Eficent, Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/manufacture-reporting',
    'license': 'AGPL-3',
    "depends": ['mrp'],
    "data": [
        'views/mrp_bom_structure_report_view.xml',
    ],
    "installable": True
}
