# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "MRP BOM Structure XLSX",
    'version': '12.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Export BoM Structure to Excel .XLSX',
    'author': "Eficent, Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/manufacture-reporting',
    'license': 'AGPL-3',
    "depends": ['report_xlsx', 'mrp'],
    "data": [
        'report/bom_structure_xlsx.xml',
    ],
    "installable": True
}
