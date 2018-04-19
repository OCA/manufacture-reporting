import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-manufacture-reporting",
    description="Meta package for oca-manufacture-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-mrp_bom_current_stock',
        'odoo9-addon-mrp_bom_structure_report_level_1',
        'odoo9-addon-mrp_bom_structure_xlsx',
        'odoo9-addon-mrp_bom_structure_xlsx_level_1',
        'odoo9-addon-report_mrp_bom_matrix',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
