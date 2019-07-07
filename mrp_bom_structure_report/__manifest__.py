# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "MRP BoM Structure Report",
    "version": "11.0.1.2.0",
    "author": "Odoo SA, Eficent, Odoo Community Association (OCA)",
    "website": "https://www.github.com/OCA/manufacture-reporting",
    "category": "Manufacture Reporting",
    "depends": [
        "mrp",
        "web",
    ],
    "data": [
        "views/mrp_bom_views.xml",
        "views/mrp_templates.xml",
        "reports/mrp_report_bom_structure.xml",
        "reports/mrp_report_views_main.xml",
    ],
    'qweb': ['static/src/xml/mrp.xml'],
    "license": "AGPL-3",
    'installable': True,
}
