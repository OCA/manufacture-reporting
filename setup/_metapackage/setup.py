import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-manufacture-reporting",
    description="Meta package for oca-manufacture-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-mrp_bom_structure_xlsx>=16.0dev,<16.1dev',
        'odoo-addon-mrp_bom_structure_xlsx_level_1>=16.0dev,<16.1dev',
        'odoo-addon-mrp_flattened_bom_xlsx>=16.0dev,<16.1dev',
        'odoo-addon-mrp_flattened_bom_xlsx_direct_materials_cost>=16.0dev,<16.1dev',
        'odoo-addon-mrp_flattened_bom_xlsx_subcontracting_cost>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
