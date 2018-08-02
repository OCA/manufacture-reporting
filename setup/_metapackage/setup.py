import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-manufacture-reporting",
    description="Meta package for oca-manufacture-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-mrp_bom_current_stock',
        'odoo11-addon-mrp_bom_matrix_report',
        'odoo11-addon-mrp_bom_structure_html',
        'odoo11-addon-mrp_bom_structure_xlsx',
        'odoo11-addon-mrp_bom_structure_xlsx_level_1',
        'odoo11-addon-mrp_flattened_bom_xlsx',
        'odoo11-addon-mrp_order_report_product_barcode',
        'odoo11-addon-mrp_order_report_stock_location',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
