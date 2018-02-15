# Copyright 2018 Camptocamp SA
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "MRP BoM Current Stock",
    "summary": "Add a report that explodes the bill of materials and show the "
               "stock available in the source location.",
    "version": "11.0.1.0.0",
    "category": "Manufacture",
    "website": "https://github.com/OCA/manufacture-reporting",
    "author": "Eficent, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "mrp_bom_location",
    ],
    "data": [
        "reports/report_mrpcurrentstock.xml",
        "wizard/bom_route_current_stock_view.xml",
    ],
}
