import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = "stock.lot"

    def _compute_traceability_line_ids(self):
        for lot in self:

            # Get the final product traceability lines
            context = {
                "active_id": lot.id,
                "model": "stock.lot",
            }
            traceability_lines = (
                self.env["stock.traceability.report"].with_context(context).get_lines()
            )

            # Find move line of the final product
            if traceability_lines:
                move_line = traceability_lines[0]
                traceability_line_ids = self.env[move_line["model"]].browse(
                    move_line["model_id"]
                )

            lines_todo = list(traceability_line_ids)
            while lines_todo:
                move_line = lines_todo.pop(0)

                # Get linked move lines of current move line
                linked_move_lines, is_used = self.env[
                    "stock.traceability.report"
                ]._get_linked_move_lines(move_line)

                if linked_move_lines:
                    traceability_line_ids += linked_move_lines

                # Get move lines for each linked line
                for line in linked_move_lines:
                    move_lines = self.env["stock.traceability.report"]._get_move_lines(
                        line
                    )
                    if move_lines:
                        traceability_line_ids += move_lines

                        # Add move lines to todo list
                        lines_todo += list(move_lines)

            lot.traceability_line_ids = traceability_line_ids

    traceability_line_ids = fields.Many2many(
        "stock.move.line", "Traceability Lines", compute=_compute_traceability_line_ids
    )

    def action_traceability_list(self):
        tree_view_id = self.env.ref("stock.view_move_line_tree").id
        form_view_id = self.env.ref("stock.view_move_line_form").id
        domain = [("id", "in", self.traceability_line_ids.ids)]
        action = {
            "type": "ir.actions.act_window",
            "views": [(tree_view_id, "tree"), (form_view_id, "form")],
            "view_mode": "tree,form",
            "name": _("Traceability List"),
            "res_model": "stock.move.line",
            "domain": domain,
        }
        return action
