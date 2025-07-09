from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LeaveExtend(models.Model):
    _inherit = "hr.leave"

    def action_approves_timeoff(self):
        for rec in self:
            if rec.state == "confirm" or rec.state == "validate1":
                rec.state = "validate"
            else:
                raise ValidationError(
                    "Có ít nhất 1 bản ghi không ở trạng thái: To Approve/Second Approval"
                )

    def action_timeoff_state_wizard(self):
        return {
            "name": "Timeoff state wizard",
            "type": "ir.actions.act_window",
            "res_model": "leave.batchupdate.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"list_leave": self.ids},
        }
