# Copyright 2018 Camptocamp SA
# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "MRP BoM Current Stock",
    "summary": "Add a report that explodes the bill of materials and show the "
    "stock available in the source location.",
    "version": "15.0.1.0.0",
    "category": "Manufacture",
    "website": "https://github.com/OCA/manufacture-reporting",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["mrp_bom_location", "report_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        "reports/report_mrpcurrentstock.xml",
        "wizard/bom_route_current_stock_view.xml",
    ],
}
