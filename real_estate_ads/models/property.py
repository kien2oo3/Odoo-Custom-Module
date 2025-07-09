from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate properties"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
        "website.published.mixin"
    ]  # Kích hoạt lưu lịch sử và gắn activity

    type_id = fields.Many2one("estate.property.type", string="Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    tag_vip_ids = fields.Many2many(
        "estate.property.tag",
        relation="estate_property_vip_tag_rel",
        column1="e_p_id",
        column2="e_p_tag_vip_id",
        string="VIP Tags",
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    offers_count = fields.Integer(
        string="Offers count", compute="_compute_offers_count"
    )
    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancel", "Cancel"),
        ],
        default="new",
    )
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date availability")
    expected_price = fields.Float(string="Expected price", tracking=True)
    best_offer = fields.Float(string="Best offer", compute="_compute_best_offer")
    selling_price = fields.Float(string="Selling price", readonly=True)
    bedrooms = fields.Integer(string="Bedroom")
    living_area = fields.Float(string="Living area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Float(string="Garden area")
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Float(
        string="Total area", compute="_compute_total_area", store=False
    )

    sales_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", domain=[("is_company", "=", True)]
    )
    buyer_email = fields.Char(string="Buyer email", related="buyer_id.email")
    buyer_phone = fields.Char(string="Buyer phone", related="buyer_id.phone")

    @api.depends("offer_ids")
    def _compute_offers_count(self):
        for rec in self:
            if rec.offer_ids:
                rec.offers_count = len(rec.offer_ids)
            else:
                rec.offers_count = False

    @api.depends("living_area", "garden", "garden_area")
    def _compute_total_area(self):
        for record in self:
            if record.garden:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = record.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(
                    list(map(lambda x: x["price"], record.offer_ids))
                )
            else:
                record.best_offer = 0

    def action_sold(self):
        print(f"Current context: {self.env.context}")
        for rec in self:
            rec.state = "sold"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"

    def action_button_property_offer_tree_view(self):
        self.ensure_one()
        return {
            "name": "Show Property Offer",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "view_mode": "tree",
            "domain": [("property_id", "=", self.id)],
        }

    def name_get(self):
        rs = []
        for pro in self:
            rs.append((pro.id, "%s(%s)" % (pro.name, pro.postcode)))
        return rs

    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = domain + [
                "|",
                ("name", operator, name),
                ("postcode", operator, name),
            ]
        full_domain = args + domain
        rs = self.search(domain=full_domain)
        return rs.name_get()

    def action_button(self):
        print("\033[32m===================> Action button called\033[0m")
        # print(self)
        # print(len(self))
        # print(self.env)
        self.env["estate.property"].action_button_model()

        #### recordset.ids
        # rcs = self.env['estate.property'].search([])
        # print(rcs.ids)

        #### self.env
        # print(self.env.user)
        # print(self.env.user.name)
        # print(self.env.user.id)
        # print(self.env.uid)
        # print(self.env.lang)
        # print(self.env.context)

        #### recordset.exists()
        # rcs = self.env['estate.property'].browse([9999])
        # if rcs.exists():
        #     print("Record id 9999 tồn tại")
        # else:
        #     print("Record id 9999 không tồn tại")

        #### recordset.ensure_one()
        # rcs = self.env['estate.property'].browse([2])
        # if rcs.ensure_one():
        #     print("True")
        # else:
        #     print("False")

        #### recordset.name_get()
        # print(self.name_get())

        #### recordset.get_metadata()
        # print(self.get_metadata()[0]["write_uid"])

        #### fields_get()
        # rs = self.env['estate.property'].fields_get()
        # print(rs)

        #### read_group()
        # rs = self.env['estate.property'].read_group(domain=[],
        #                                             fields=['garden', 'postcode', 'expected_price:sum'],
        #                                             groupby=['garden', 'postcode'], lazy=False)
        # print(rs)

        #### read()
        # rs = self.env['estate.property'].search([('expected_price','>=',1500)]).read(["name","postcode"])
        # print(rs)

        #### Test search
        # properties = self.env["estate.property"].search(domain=[('expected_price', '>=', 1500), ('garden', '=', True)],
        #                                                 limit=2, order='expected_price desc', offset=0)
        # print(properties)
        # for rec in properties:
        #     print(rec.mapped('name'))
        #     print(rec.id)
        #     print(rec.name)
        #     print(rec.expected_price)
        #     print(rec.garden)

        ##### Test search_count
        # property_count = self.env['estate.property'].search_count(domain=[('garden', '=', True)])
        # print(property_count)

        ##### Test browse and exists
        # properties = self.env['estate.property'].browse([2,3,999])
        # print(properties.exists())

        ##### Test name_search
        # rs = self.env['estate.property'].name_search(name='Villa', args=[('expected_price', '>=', 1500)],
        #                                              operator="like")
        # for pro in rs:
        #     print(pro[0])

        # rs1 = self.env['estate.property'].name_search(name='Villa')
        # print(rs1)

    @api.model
    def action_button_model(self):
        print("\033[32m===================> Action button called\033[0m")
        print("User ID:", self.env.uid)
        print("User record:", self.env.user)
        print("Company:", self.env.company.name)
        print("Context:", self.env.context)  # Đây là dict ✔
        print("Lang:", self.env.context.get("lang"))
        print("Active ID:", self.env.context.get("active_id"))
        print("Available models:", dir(self.env))  # Gợi ý tên model có thể truy cập

    def action_button_url(self):
        return {
            "type":"ir.actions.act_url",
            "name":"Odoo",
            "url":"https://youtube.com",
            "target":"self"
        }
    
    def _compute_website_url(self):
        for rec in self:
            rec.website_url = f"/property/{rec.id}"


# @api.onchange("best_offer", "name")
# def onchange_best_offer(self):
#     print("OnChange called")
#     print(self)
#     print(type(self))
#     return {
#         'warning': {
#             'title': "Best offer Update",
#             'message': "Best offer updated!"
#         }
#     }


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

    # @api.model_create_multi
    # def create(self, vals_list):
    #     print("Create type called")
    #     print(self)
    #     print(self.env['res.partner'].search([('is_company', '=', True)]).mapped('phone'))
    #     print(vals_list)
    #     type = self.browse(3)
    #     print(type.name)
    #     return super().create(vals_list)

    # def write(self, vals):
    #     print(self)
    #     print(self.env)
    #     print(self.env['res.partner'].search([('is_company', '=', True)]).mapped('phone'))
    #     print(vals)
    #     return super().write(vals)


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color Index")
