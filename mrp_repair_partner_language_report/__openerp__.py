# -*- coding: utf-8 -*-
# © 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Repair orders in partner language",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://www.agilebg.com",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mrp_repair",
    ],
    "data": [
        "mrp_repair_report.xml",
        "views/report_mrp_repair_order.xml",
    ],
}
