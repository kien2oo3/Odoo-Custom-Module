from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EmployeesExperienceYearWizard(models.TransientModel):
    _name = "employees.experience.year.wizards"
    _description = "Employees experience year wizards"

    employee_ids = fields.Many2many("hr.employee", string="Employees", required=True)
    experience_years = fields.Integer(string="Experience years", required=True)

    @api.onchange('experience_years')
    def _onchange_experince_year(self):
        for rec in self:
            if rec.experience_years:
                if rec.experience_years < 0 or rec.experience_years >30:
                    raise ValidationError("Năm kinh nghiệm không được âm và không vượt quá 30 năm!")

    def action_confirm_experience_year(self):
        self.ensure_one()
        for employee in self.employee_ids:
            employee.years_of_experience = self.experience_years
