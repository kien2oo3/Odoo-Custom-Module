from odoo import fields, models, api
from odoo.exceptions import ValidationError

class LeaveRequest(models.Model):
    _name = 'leave.request'
    _description = 'Leave request'

    employee_id = fields.Many2one('res.users', string='Employee')
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    reason = fields.Text(string='Reason')
    state = fields.Selection(string="State",
                             selection=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'),
                                        ('refused', 'Refused')])
    number_of_days = fields.Integer(string='Number of days', compute='_compute_number_of_days')

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
