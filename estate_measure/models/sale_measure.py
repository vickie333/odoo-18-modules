from odoo import models, fields

class EstateMeasure(models.Model):
    _inherit = ['sale.order']

    area = fields.Float(string="Area (sqm)")
    price_per_sqm = fields.Float(string="Price per sqm")


