from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Customer")
    property_id = fields.Many2one("estate.property", string="Property")
    deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline", store=True)
    validity = fields.Integer(string="Validity")
    creation_date = fields.Date(string="Creation date")

    @api.depends("validity", "creation_date")
    def _compute_deadline(self):
        for record in self:
            if record.creation_date:
                record.deadline = record.creation_date + timedelta(days=record.validity)
            else:
                record.deadline = False

    @api.depends("deadline", "creation_date")
    def _inverse_deadline(self):
        for record in self:
            if record.deadline and record.creation_date:
                record.validity = (record.deadline - record.creation_date).days

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if not val.get('creation_date'):
                val['creation_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)

    @api.constrains("validity")
    def constrain_validity(self):
        print("Constrain called")
        print(self)
        for record in self:
            if record.validity < 0:
                raise ValidationError("Trường Validity không được phép âm!")