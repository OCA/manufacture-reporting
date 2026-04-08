# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "MRP Production Component XLSX Report",
    "summary": "Print aggregated component list for selected "
    "Manufacturing Orders to XLSX",
    "version": "18.0.1.0.0",
    "category": "Manufacturing",
    "author": "Cetmix, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/manufacture-reporting",
    "license": "AGPL-3",
    "depends": ["mrp", "report_xlsx_helper"],
    "data": [
        "report/component_report_xlsx.xml",
    ],
}
