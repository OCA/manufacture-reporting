.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

==============================================
Product Barcode on the Production Order Report
==============================================

This module adds the product code or lot/serial number barcode on the production order report so that manufacturing users can scan barcodes.

Configuration
=============

* Check the configuration of your products to make sure:
  * the barcode field is set
  * the tracking is configured: No tracking, By Lot Number, By Serial Number
* Create a BOM using these products

Usage
=====

* Create a manufacturing order for the BOM created above
* Print the Production Order

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
    :alt: Try me on Runbot
    :target: https://runbot.odoo-community.org/runbot/131/11.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/manufacture-reporting/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted it
first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Maxime Chambreuil <mchambreuil@opensourceintegrators.com>


Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
