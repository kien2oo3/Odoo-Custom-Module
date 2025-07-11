from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.fields import One2many


class Employee(models.Model):
    _inherit = "hr.employee"
    review_ids = One2many(
        "hr.performance.review", "employee_id", string="Performance reviews"
    )
    reviews_count = fields.Integer(
        string="Reviews count", compute="_compute_reviews_count"
    )
    average_score = fields.Float(
        string="Average score", compute="_compute_average_score"
    )
    years_of_experience = fields.Integer(string="Years of experience")

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            if "years_of_experience" in record.keys():
                if (
                    record["years_of_experience"] < 0
                    or record["years_of_experience"] > 30
                ):
                    raise ValidationError(
                        "Năm kinh nghiệm không được âm và không vượt quá 30 năm!"
                    )
        return super().create(vals)

    def write(self, vals):
        if "years_of_experience" in vals.keys():
            if vals["years_of_experience"] < 0 or vals["years_of_experience"] > 30:
                raise ValidationError(
                    "Năm kinh nghiệm không được âm và không vượt quá 30 năm!"
                )
        return super().write(vals)

    @api.depends("review_ids")
    def _compute_reviews_count(self):
        for rec in self:
            if rec.review_ids:
                rec.reviews_count = len(rec.review_ids)
            else:
                rec.reviews_count = 0

    @api.depends("review_ids")
    def _compute_average_score(self):
        for rec in self:
            average = 0
            i = 0
            if rec.review_ids:
                list_score = rec.review_ids.search([("state", "=", "approved")])
                for score in list_score:
                    if score.performance_score:
                        average = average + score.performance_score
                        i = i + 1
            if i == 0:
                rec.average_score = 0
            else:
                rec.average_score = average / i

    # Hàm hiển thị popup wizards cập nhật số năm kinh nghiệm nhân viên
    def action_open_experience_year_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Experience year wizards",
            "res_model": "hr.employee.experience.year.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"ex_years": self.years_of_experience},
            # "context": {
            #     "default_employee_id": self.id,
            #     "default_experience_years": self.years_of_experience,
            # },
        }

    def action_button_performance_review_tree_view(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": f"Show reviews of {self.name}",
            "res_model": "hr.performance.review",
            "view_mode": "tree",
            "domain": [("employee_id", "=", self.id)],
        }

    # Hàm hiển thị action hiện wizards để update năm kinh nghiệm cho list employee
    def show_experience_year_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Experience year wizards",
            "res_model": "employees.experience.year.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_employee_ids": self.ids},
        }


class PerformanceReview(models.Model):
    _name = "hr.performance.review"
    _description = "hr performance review"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]  # Kích hoạt lưu lịch sử và gắn activity

    name = fields.Char(string="Name", required=True)
    def _get_employee_default(self):
        print("=================================v==========================")
        print(self.env.context.get("uid"))
        return self.env["hr.employee"].search([('user_id','=',self.env.context.get("uid"))])
    employee_id = fields.Many2one("hr.employee", string="Employee", default=_get_employee_default)
    review_date = fields.Date(string="Review date")
    reviewer_id = fields.Many2one("res.users", string="Reviewer")
    performance_score = fields.Float(string="Score")
    comments = fields.Text(string="Comments")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
        ],
        string="Sate",
        default="draft",
        tracking=True,
    )

    is_employee = fields.Boolean(
        string="Is employee", store=False, compute="_compute_is_employee"
    )

    @api.depends("reviewer_id")
    def _compute_is_employee(self):
        print("========================================================>Compute called")
        for rec in self:
            if (
                self.env.user.has_group("performance_review_management.group_employee")
                and not self.env.user.has_group(
                    "performance_review_management.group_manager"
                )
                and not self.env.user.has_group(
                    "performance_review_management.group_admin"
                )
            ):
                rec.is_employee = True
            else:
                rec.is_employee = False

    # @api.onchange("reviewer_id")
    # def _onchange_is_employee(self):
    #     print("========================================================>Onchange called")
    #     print("========================================================>Onchange called")
    #     print("========================================================>Onchange called")
    #     for rec in self:
    #         if (
    #             self.env.user.has_group("performance_review_management.group_employee")
    #             and not self.env.user.has_group(
    #                 "performance_review_management.group_manager"
    #             )
    #             and not self.env.user.has_group(
    #                 "performance_review_management.group_admin"
    #             )
    #         ):
    #             rec.is_employee = True
    #         else:
    #             rec.is_employee = False

    # @api.depends('review_date')
    # def _compute_review_date(self):
    #     for rec in self:
    #         if rec.review_date:
    #             if fields.Date.today() > rec.review_date:
    #                 raise ValidationError("Ngày đánh giá không được nhỏ hơn ngày hiện tại")

    @api.constrains("review_date")
    def _constrain_review_date(self):
        for rec in self:
            if rec.review_date:
                if fields.Date.today() > rec.review_date:
                    raise ValidationError(
                        "Ngày đánh giá không được nhỏ hơn ngày hiện tại"
                    )

    def action_submit(self):
        for rec in self:
            if rec.state == "draft":
                rec.state = "submitted"
            else:
                raise ValidationError(
                    "Không thể gửi đơn vì đơn không ở trạng thái bản nháp!"
                )

    def action_approve(self):
        for rec in self:
            if rec.state == "submitted":
                if (
                    self.env.user.has_group(
                        "performance_review_management.group_manager"
                    )
                    and not self.env.user.has_group(
                        "performance_review_management.group_admin"
                    )
                    and self.env.uid != rec.reviewer_id.id
                ):
                    raise ValidationError(
                        "Bạn không thể approve đơn đánh giá của người quản lý khác!"
                    )
                rec.state = "approved"
            else:
                raise ValidationError(
                    "Không thể chấp nhận đơn vì đơn không ở trạng thái đã gửi!"
                )
