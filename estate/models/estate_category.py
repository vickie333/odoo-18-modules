from odoo import models, fields

class EstateCategory(models.Model):
    _name = 'estate.category'
    _description = 'Estate Category'

    name = fields.Char(string='Name',required=True)
    #property_ids = fields.One2many('estate.estate','category_id',string='Properties')
    