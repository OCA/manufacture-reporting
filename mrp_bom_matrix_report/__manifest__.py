# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BOM Matrix Report",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Eficent,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/manufacture-reporting",
    "category": "Manufacturing",
    "depends": [
        "mrp",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_bom_matrix_report_views.xml",
    ],
}
