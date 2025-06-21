from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate properties"

    type_id = fields.Many2one("estate.property.type", string="Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date availability")
    expected_price = fields.Float(string="Expected price")
    best_offer = fields.Float(string="Best offer", compute="_compute_best_offer")
    selling_price = fields.Float(string="Selling price")
    bedrooms = fields.Integer(string="Bedroom")
    living_area = fields.Float(string="Living area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Float(string="Garden area")
    garden_orientation = fields.Selection(string="Garden orientation",
                                          selection=[("north", "North"), ("south", "South"), ("east", "East"),
                                                     ("west", "West")])
    total_area = fields.Float(string="Total area", compute="_compute_total_area", store=False)

    sales_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer",
                               domain=[('is_company', '=', True), ('city', '=', 'Tracy')])
    buyer_email = fields.Char(string="Buyer email", related="buyer_id.email")
    buyer_phone = fields.Char(string="Buyer phone", related="buyer_id.phone")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(list(map(lambda x: x['price'], record.offer_ids)))

    @api.onchange("best_offer", "name")
    def onchange_best_offer(self):
        print("OnChange called")
        print(self)
        print(type(self))
        return {
            'warning': {
                'title': "Best offer Update",
                'message': "Best offer updated!"
            }
        }


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"

    name = fields.Char(string="Name", required=True)

    @api.constrains("name")
    def _constrains_name(self):
        print("Constrains name called")
        for rec in self:
            if len(rec.name) <= 3:
                raise ValidationError("Tên không được nhỏ hơn 3 ký tự!")

    @api.model_create_multi
    def create(self, vals_list):
        print("Create type called")
        print(self)
        print(self.env['res.partner'].search([('is_company','=',True)]).mapped('phone'))
        print(vals_list)
        type = self.browse(3)
        print(type.name)
        return super().create(vals_list)

    def write(self, vals):
        print(self)
        print(self.env)
        print(self.env['res.partner'].search([('is_company', '=', True)]).mapped('phone'))
        print(vals)
        return super().write(vals)

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color Index")
