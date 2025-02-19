# Copyright 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Display Component's Reserved Lots on the Production Order Report",
    "version": "16.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/manufacture-reporting",
    "license": "AGPL-3",
    "maintainers": ["ivantodorovich"],
    "category": "Manufacturing",
    "depends": [
        "mrp_order_report_lot",
        "mrp_order_report_reserved",
    ],
    "data": ["reports/mrp_order_report.xml"],
    "auto_install": True,
}
