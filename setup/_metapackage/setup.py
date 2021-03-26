import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-manufacture-reporting",
    description="Meta package for oca-manufacture-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-mrp_bom_structure_xlsx',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
