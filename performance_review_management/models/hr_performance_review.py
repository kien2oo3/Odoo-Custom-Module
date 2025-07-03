from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.fields import One2many


class Employee(models.Model):
    _inherit = 'hr.employee'
    review_ids = One2many('hr.performance.review', 'employee_id', string='Performance reviews')
    reviews_count = fields.Integer(string="Reviews count", compute='_compute_reviews_count')
    average_score = fields.Float(string="Average score", compute='_compute_average_score')

    @api.depends('review_ids')
    def _compute_reviews_count(self):
        for rec in self:
            if rec.review_ids:
                rec.reviews_count = len(rec.review_ids)
            else:
                rec.reviews_count = 0

    @api.depends('review_ids')
    def _compute_average_score(self):
        for rec in self:
            average = 0
            i = 0
            if rec.review_ids:
                list_score = rec.review_ids.search([('state', '=', 'approved')])
                for score in list_score:
                    if score.performance_score:
                        average = average + score.performance_score
                        i = i + 1
            if i == 0:
                rec.average_score = 0
            else:
                rec.average_score = average / i

    def action_button_performance_review_tree_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Show reviews of {self.name}',
            'res_model': 'hr.performance.review',
            'view_mode': 'tree',
            'domain': [('employee_id', '=', self.id)]
        }


class PerformanceReview(models.Model):
    _name = 'hr.performance.review'
    _description = 'hr performance review'

    name = fields.Char(string="Name", required=True)
    employee_id = fields.Many2one("hr.employee", string="Employee")
    review_date = fields.Date(string="Review date")
    reviewer_id = fields.Many2one("res.users", string="Reviewer")
    performance_score = fields.Float(string="Score")
    comments = fields.Text(string="Comments")
    state = fields.Selection(selection=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved')],
                             string="Sate", default="draft")

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
                    raise ValidationError("Ngày đánh giá không được nhỏ hơn ngày hiện tại")

    def action_submit(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'submitted'
            else:
                raise ValidationError("Không thể gửi đơn vì đơn không ở trạng thái bản nháp!")

    def action_approve(self):
        for rec in self:
            if rec.state == 'submitted':
                if self.env.user.has_group(
                        'performance_review_management.group_manager') and not self.env.user.has_group(
                    'performance_review_management.group_admin') and self.env.uid != rec.reviewer_id.id:
                    raise ValidationError("Bạn không thể approve đơn đánh giá của người quản lý khác!")
                rec.state = 'approved'
            else:
                raise ValidationError("Không thể chấp nhận đơn vì đơn không ở trạng thái đã gửi!")
