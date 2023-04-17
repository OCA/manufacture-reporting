import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-manufacture-reporting",
    description="Meta package for oca-manufacture-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-mrp_bom_current_stock',
        'odoo14-addon-mrp_bom_structure_xlsx',
        'odoo14-addon-mrp_bom_structure_xlsx_level_1',
        'odoo14-addon-mrp_flattened_bom_xlsx',
        'odoo14-addon-mrp_flattened_bom_xlsx_direct_materials_cost',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
