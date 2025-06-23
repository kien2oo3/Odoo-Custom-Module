from odoo import fields, models, api
from odoo.exceptions import ValidationError


class LeaveRequest(models.Model):
    _name = 'leave.request'
    _description = 'Leave request'

    employee_id = fields.Many2one('res.users', string='Employee', default=lambda self: self.env.user)
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    reason = fields.Text(string='Reason')
    state = fields.Selection(string="State",
                             selection=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'),
                                        ('refused', 'Refused')], default='draft')
    number_of_days = fields.Integer(string='Number of days', compute='_compute_number_of_days')
    is_employee_user = fields.Boolean(string="Is employee user", default=False, compute='_compute_is_employee_user',
                                      store=False)

    @api.depends('start_date', 'end_date')
    def _compute_number_of_days(self):
        for rc in self:
            if rc.start_date and rc.end_date:
                if rc.start_date <= rc.end_date:
                    rc.number_of_days = (rc.end_date - rc.start_date).days
                else:
                    raise ValidationError("Ngày bắt đầu nghỉ phải nhỏ hơn hoặc bằng ngày kết thúc nghỉ!")
            else:
                rc.number_of_days = 0

    @api.depends('employee_id')
    @api.depends_context('uid')
    def _compute_is_employee_user(self):
        for rc in self:
            rc.is_employee_user = self.env.user.has_group('leave_management.group_employee_user') and not self.env.user.has_group('leave_management.group_employee_manager')

    def action_submit(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError('Đơn ở trạng thái bản nháp mới được phép gửi!')
            else:
                rec.state = 'submitted'

    def action_approve(self):
        for rec in self:
            if self.env.user.has_group('leave_management.group_employee_user') and not self.env.user.has_group('leave_management.group_employee_manager'):
                raise ValidationError('Bạn không có quyền ấn nút chấp thuận!')
            if rec.state != 'submitted':
                raise ValidationError('Đơn ở trạng thái đã gửi mới được phép chấp nhận!')
            else:
                rec.state = 'approved'

    def action_refuse(self):
        for rec in self:
            if rec.state != 'submitted':
                raise ValidationError('Đơn ở trạng thái đã gửi mới được phép từ chối!')
            else:
                rec.state = 'refused'