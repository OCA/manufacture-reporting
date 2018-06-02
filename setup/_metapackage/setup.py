import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-manufacture-reporting",
    description="Meta package for oca-manufacture-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-mrp_bom_current_stock',
        'odoo10-addon-mrp_bom_matrix_report',
        'odoo10-addon-mrp_bom_structure_report_level_1',
        'odoo10-addon-mrp_bom_structure_xlsx',
        'odoo10-addon-mrp_bom_structure_xlsx_level_1',
        'odoo10-addon-mrp_flattened_bom_xlsx',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
