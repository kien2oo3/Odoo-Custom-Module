from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class AbstractPropertyOffer(models.AbstractModel):
    _name = "abstract.property.offer"
    _description = "Abstract property offer"

    phone = fields.Char("Phone")
    email = fields.Char("Email")


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"
    _inherit = "abstract.property.offer"

    name = fields.Char(string="Name", compute="_compute_name")
    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status", selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", string="Customer")
    property_id = fields.Many2one("estate.property", string="Property")
    deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=True,
    )
    validity = fields.Integer(string="Validity", default=7)

    def creation_date_default(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Creation date", default=creation_date_default)

    @api.depends("partner_id", "property_id")
    def _compute_name(self):
        for rec in self:
            if rec.partner_id and rec.property_id:
                rec.name = f"{rec.partner_id.name} - {rec.property_id.name}"
            else:
                rec.name = False

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
            if not val.get("creation_date"):
                val["creation_date"] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)

    @api.constrains("validity")
    def constrain_validity(self):
        print("Constrain called")
        print(self)
        for record in self:
            if record.validity < 0:
                raise ValidationError("Trường Validity không được phép âm!")

    def action_accept_offer(self):
        self.ensure_one()
        offers = self.env["estate.property.offer"].search(
            [
                ("id", "!=", self.id),
                ("status", "=", "accepted"),
                ("property_id", "=", self.property_id.id),
            ]
        )
        if offers:
            raise ValidationError(
                "Bạn đã chấp nhận 1 Offer khác, vui lòng từ chối nó để tiếp tục!"
            )
        if self.property_id:
            self.property_id.selling_price = self.price
        self.status = "accepted"
        self.property_id.state = "accepted"

    def action_refuse_offer(self):
        self.ensure_one()
        if not self.env["estate.property.offer"].search(
            [
                ("id", "!=", self.id),
                ("property_id", "=", self.property_id.id),
                ("status", "=", "accepted"),
            ]
        ):
            self.property_id.selling_price = 0
        self.status = "refused"
        self.property_id.state = "received"

    def extend_deadline_validity(self):
        print("Extend deadline validity called")
        print(self.ids)
        ids = self.ids
        if ids:
            offers = self.env["estate.property.offer"].browse(ids).exists()
            for offer in offers:
                offer.validity = 7

    def _cron_extend_validity_property_offer(self):
        offers = self.env["estate.property.offer"].search([])
        if offers:
            for offer in offers:
                if offer.validity:
                    offer.validity = offer.validity + 1
