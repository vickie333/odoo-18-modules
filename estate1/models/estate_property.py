from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
    ('check_expected_price','CHECK(expected_price > 0)',
     'The expected price must be positive.'),
    ('check_selling_price','CHECK(selling_price > 0)',
     'The selling price must be positive.'),
]

    name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='PostCode')
    date_availability = fields.Date(copy=False, default=lambda self: (date.today() + timedelta(days=90)), tracking=True)
    expected_price = fields.Float(string='Expected Price', required=True, default=0.0, tracking=True)
    selling_price = fields.Float(string='Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    living_area = fields.Integer(default=0, string="Living Area(sqm)")
    tags_ids = fields.Many2many('estate.property.tags', string='Tags')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user, tracking=True)
    facades = fields.Integer(default=0)
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection([
        ('north','North'), 
        ('south','South'), 
        ('east','East'), 
        ('west','West')
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new','New'),
        ('offer_received','Offer Received'),
        ('offer_accepted','Offer Accepted'),
        ('sold','Sold'),
        ('canceled','Canceled')
    ], default="new", copy=False, tracking=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(string="Total Area(sqm)", default=0.0, compute="_compute_total_area")
    best_price = fields.Float(string="Best Price",compute="_compute_best_price")


    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def action_cancel_property(self):
        for property in self:
            if property.state != "sold":
                property.state = 'canceled'
            else:
                raise UserError("You cannot cancel a property that is already sold.")

    def action_sold_property(self):
        for property in self:
            if property.state != "canceled":
                property.state = 'sold'
            else:
                raise UserError("You cannot sell a property that is already canceled.")
            

    @api.constrains('expected_price','selling_price')
    def _check_price(self):
        for property in self:
            if property.expected_price <= 0:
                raise ValidationError("The expected price must be positive.")
            if property.selling_price < 0:
                raise ValidationError("The selling price must be positive.")

    @api.constrains('expected_price','selling_price')
    def _validate_selling_price(self):
        for offer in self:
            accepted_offers = offer.offer_ids.filtered(lambda o: o.status == 'accepted')

            if accepted_offers:
                if offer.selling_price < (offer.expected_price * 0.9):
                    raise ValidationError("The selling price must be at least 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def unlink(self):
        for property in self:
            if property.offer_ids:
                raise UserError("You cannot delete a property with offers.")
            if property.state not in ['new','canceled']:
                raise UserError("Only new and cancelled properties can be deleted.")
  
        return super().unlink()


