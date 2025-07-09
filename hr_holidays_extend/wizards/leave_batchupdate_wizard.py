from odoo import fields, models, api


class LeaveBatchupdateWizard(models.TransientModel):
    _name = "leave.batchupdate.wizard"
    _description = "leave batchupdate wizard"

    state = fields.Selection(
        [
            ("draft", "To Submit"),
            ("confirm", "To Approve"),
            ("refuse", "Refused"),
            ("validate1", "Second Approval"),
            ("validate", "Approved"),
        ],
        string="Status",
        help="The status is set to 'To Submit', when a time off request is created."
        + "\nThe status is 'To Approve', when time off request is confirmed by user."
        + "\nThe status is 'Refused', when time off request is refused by manager."
        + "\nThe status is 'Approved', when time off request is approved by manager.",
    )

    def button_update_timeoff_state(self):
        # print(self.env.context.get("list_leave"))
        # print(type(self.env.context.get("list_leave")))
        list_ids = self.env.context.get("list_leave")
        self.env["hr.leave"].browse(list_ids).exists().write({"state": self.state})
