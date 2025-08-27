from odoo import models, fields, api

class Estate(models.Model):
    _name = 'estate.estate'
    _description = 'Estate'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name',required=True,tracking=True)
    description = fields.Html()
    price = fields.Float(string='Price',required=True,default=0.0,tracking=True)
    bedrooms = fields.Integer(string='Bedrooms',default=1)
    bathrooms = fields.Integer(string='Bathrooms',default=1)
    state = fields.Selection([('new','New'),('offer_received','Offer Received'),('sold','Sold')],default='new')
    living_area = fields.Integer(string='Living Area')
    for_sale = fields.Boolean(string='For Sale',compute='_compute_for_sale')
    currency_id = fields.Many2one('res.currency',default=lambda self: self.env.company.currency_id,tracking=True)
    category_id = fields.Many2one('estate.category')
    date_availability = fields.Date(default=lambda self: fields.Date.today())
    owners_ids = fields.Many2many('res.partner')
    images_ids = fields.One2many('estate.image','estate_id',string='Images')

    @api.depends('state')
    def _compute_for_sale(self):
        for estate in self:
            estate.for_sale = True if estate.state in ['new','offer_received'] else False

    @api.constrains('price')
    def _check_price(self):
        for estate in self:
            if estate.price <= 0:
                raise models.ValidationError('Price must be positive')

    @api.constrains("category_id")
    def _check_category(self):
        for estate in self:          #estamos haciendo referencia al objeto mansion del modulo estate creado en data_estate_category.xml
            if estate.category_id.id == self.env.ref('estate.category_mansion').id:
                if estate.bedrooms < 4:
                    raise models.ValidationError(
                        "Mansion must have at least 4 bedrooms"
                        )

    def create(self,vals):
        vals['name'] = f"{vals['name']} - {self.env.company.name}"
        res = super().create(vals)
        return res

    def write(self,vals):
        res = super().write(vals)
        return res

    def unlink(self):
        for estate in self:
            if estate.state == 'sold':
                raise models.ValidationError('You cannot delete a sold property')
        return super().unlink()