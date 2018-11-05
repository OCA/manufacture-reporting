.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

=====================================
MRP Flattened BOM Report XLSX
=====================================

This module extends the functionality of the MRP capabilities of Odoo,
and allows you to export the flattened BOM to MS Excel .XLSX format.

A flattened bill of material removes the intermediate levels in the BOM
and connect the lowest levels directly to the highest level.

A list of the sum of lowest levels will be shown for every
BoM you export using this method.

It also maintains units correctly across all nested BOM's and take units
that have been defined in product Unit of Measure field.


Usage
=====

To use this module, you need to:

#. Go to 'Manufacturing / Products / Bill of Materials'

#. Select a BOM or more BOMS 

   *(Could be interesting to modify quantities of these BOMs)*

#. Go to 'Print / Export Flattened BOM to Excel'.

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

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Héctor Villarreal <hector.villarreal@eficent.com>
* Lois Rilo <lois.rilo@eficent.com>


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
