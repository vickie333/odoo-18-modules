from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    estate_id = fields.Many2one('estate.estate', 'Estate')