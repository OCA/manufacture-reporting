Adds a PDF report to print BoM(s) in a very simple way.

.. figure:: ../static/description/bom_simple_report_new_action.jpeg

.. figure:: ../static/description/bom_simple_report_new_report.png

Compatible with [mrp_bom_widget_section_and_note_one2many](https://github.com/OCA/manufacture/tree/16.0/mrp_bom_widget_section_and_note_one2many)

Also compatible for being called in parent template. For this purpose, you need
to set params with t-set :
t-set="docs" → BoM
t-set="bom_intermediate_parent_bom_text" → nested BoM could be printed
t-set="bom_qty" → desired BoM quantity

Call this template with t-foreach to print multiple BoM with multiple BoM quantity
→ Example in grap-odoo-custom module : mrp_bom_wizard_production