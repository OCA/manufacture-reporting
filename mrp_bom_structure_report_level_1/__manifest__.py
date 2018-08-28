# © 2017 Eficent Business and IT Consulting Services S.L.
#        (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BOM Structure Report Level 1",
    "version": "11.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/manufacture-reporting",
    "category": "Manufacture",
    "depends": ["mrp"],
    "data": [
        "views/report_mrpbomstructure.xml",
        "views/mrp_bom_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
