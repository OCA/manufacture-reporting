import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-manufacture-reporting",
    description="Meta package for oca-manufacture-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-mrp_bom_current_stock>=15.0dev,<15.1dev',
        'odoo-addon-mrp_flattened_bom_xlsx>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
