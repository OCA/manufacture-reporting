# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, tools, api


class MrpBomMatrixReport(models.Model):
    _name = 'mrp.bom.matrix.report'
    _auto = False

    component_id = fields.Many2one(
        comodel_name='product.product',
        string='Component Product',
        readonly=True,
    )
    parent_template_id = fields.Many2one(
        comodel_name='product.template',
        string='Parent Product Template',
        readonly=True,
    )
    parent_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Parent Product Category',
        store=True,
        readonly=True,
    )
    count_parent_usage = fields.Integer(
        string='# Uses in Parent',
        readonly=True,
    )

    def _select(self):
        select_str = """
            SELECT min(l.id) as id, l.product_id as component_id,
                   p.product_tmpl_id as parent_template_id,
                   CASE WHEN min(q.count_parent_usage) is null
                   THEN 1
                   ELSE min(q.count_parent_usage)
                   END as count_parent_usage,
                   pt.categ_id as parent_category_id
        """
        return select_str

    def _from(self):
        # In this part we search recursively for the top parent product for
        # all the BOMs where the component is used.
        from_str = """
            FROM mrp_bom_line as l
            INNER JOIN mrp_bom p
            ON p.id = l.bom_id
            INNER JOIN product_template pt
            on pt.id = p.product_tmpl_id
            LEFT JOIN (
                WITH RECURSIVE tree(child, child_name, root, root_name) AS (
                    WITH cte1 AS (
                    SELECT	pt1.id as child_id,
                        pt2.id as parent_id,
                        pt1.name as child_name,
                        pt2.name as parent_name
                    FROM mrp_bom_line as l
                        INNER JOIN product_product as pr
                        ON pr.id = l.product_id
                        INNER JOIN product_template as pt1
                        ON pt1.id = pr.product_tmpl_id
                        INNER JOIN mrp_bom as p1
                        ON p1.id = l.bom_id
                        INNER JOIN product_template as pt2
                        ON pt2.id = p1.product_tmpl_id)

                    SELECT  c.child_id,
                        c.child_name,
                        c.parent_id,
                        c.parent_name
                        FROM cte1 as c
                        LEFT JOIN cte1 as p
                        ON c.parent_id = p.child_id
                        WHERE p.child_id IS NULL
                        UNION
                        SELECT cte1.child_id, cte1.child_name, root, root_name
                    FROM tree
                    INNER JOIN cte1 on tree.child = cte1.parent_id)

                SELECT child, count(root_name) as count_parent_usage
                FROM tree
                group by child) as q
            ON q.child = p.product_tmpl_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY l.product_id,
                     p.product_tmpl_id,
                     pt.categ_id
        """
        return group_by_str

    def _where(self):
        where_str = """"""
        return where_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=E8103
        self._cr.execute(
            """CREATE or REPLACE VIEW {} as (
            {}
            {}
            {}
            {}
            )""".format(
                self._table,
                self._select(),
                self._from(),
                self._where(),
                self._group_by(),
            )
        )
