from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EmployeeExperienceYearWizard(models.TransientModel):
    _name = "hr.employee.experience.year.wizards"
    _description = "hr employee experience year wizards"

    def _get_employee_default(self):
        return self.env.context.get("active_id")
    employee_id = fields.Many2one("hr.employee", string="Employee", required=True, default=_get_employee_default)
    experience_years = fields.Integer(string="Experience years", required=True, default=lambda self:self.env.context.get("ex_years"))

    @api.onchange('experience_years')
    def _onchange_experince_year(self):
        for rec in self:
            if rec.experience_years:
                if rec.experience_years < 0 or rec.experience_years >30:
                    raise ValidationError("Năm kinh nghiệm không được âm và không vượt quá 30 năm!")
                
    @api.model
    def default_get(self, fields):
        print("📌 Context when opening wizards:")
        print(self.env.context)
        return super().default_get(fields)
    

    def action_confirm_experience_year(self):
        print("======================================>")
        print(self.env.context.get("active_id"))
        print(self.env.context.get("active_model"))
        print("======================================>")
        for rec in self:
            rec.employee_id.years_of_experience = rec.experience_years

