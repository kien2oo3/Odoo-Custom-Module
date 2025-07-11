from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AttendanceRequest(models.Model):
    _name = "attendance.request"
    _description = "Attendance request"

    # Tên phiếu yêu cầu
    name = fields.Char(string="Name")

    # Ngày yêu cầu
    def _set_request_date(self):
        return fields.Date.today()

    request_date = fields.Date(string="Request date", default=_set_request_date)

    # Người yêu cầu
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        default=lambda self: self.env["hr.employee"].search(
            [("user_id", "=", self.env.context.get("uid"))]
        ),
    )

    # Loại yêu cầu
    request_type = fields.Selection(
        string="Request type",
        selection=[
            ("check_in_morning", "Check in sáng"),
            ("check_out_morning", "Check out sáng"),
            ("check_in_afternoon", "Check in chiều"),
            ("check_out_afternoon", "Check out chiều"),
        ],
    )

    # Lý do
    reason = fields.Text(string="Reason")

    # Trạng thái
    state = fields.Selection(
        string="Sate",
        selection=[
            ("draft", "Nháp"),
            ("waiting", "Chờ duyệt"),
            ("approved", "Đã duyệt"),
            ("rejected", "Từ chối"),
        ],
        default="draft",
    )

    # Trường kiểm tra có là user không
    @api.depends("employee_id")
    def _compute_is_user(self):
        for rec in self:
            rec.is_user = self.env.user.has_group(
                "attendance_management.group_employee_user_attendance"
            )

    is_user = fields.Boolean(string="Is user", store=False, compute=_compute_is_user)

    @api.constrains("request_type", "employee_id", "request_date", "state")
    def check_attendance_request_unique(self):
        for rec in self:
            rs = self.env["attendance.request"].search_count(
                [
                    ("id", "!=", rec.id),
                    ("request_type", "=", rec.request_type),
                    ("employee_id", "=", rec.employee_id.id),
                    ("request_date", "=", rec.request_date),
                    ("state", "!=", "rejected"),
                ]
            )
            # print(f"rs = {rs}")
            if rs > 0:
                raise ValidationError(
                    "Đã có phiếu yêu cầu trùng với phiếu yêu cầu của bạn!"
                )

    @api.model_create_multi
    def create(self, vals):
        recs = super().create(vals)
        for rec in recs:
            rec.name = f"{rec.employee_id.name} yêu cầu bù công ngày {rec.request_date}"
            rec.state = "waiting"
        return recs

    def action_approve(self):
        for rec in self:
            if rec.state != "waiting":
                raise ValidationError(
                    "Không thể chấp nhận đơn do đơn chưa ở trạng thái chờ duyệt!"
                )
            rec.state = "approved"

    def action_refuse(self):
        for rec in self:
            if rec.state != "waiting":
                raise ValidationError(
                    "Không thể từ chối đơn do đơn chưa ở trạng thái chờ duyệt!"
                )
            rec.state = "rejected"
