from odoo import models, fields 

class EstateImage(models.Model):
    _name = 'estate.property.image'
    _description = 'Estate Property Image'

    name = fields.Char(string='Image Name', required=True)
    activity_state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned')],
        default='overdue')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')],
        default='draft', string='State')
    date_order = fields.Date(string='Order Date', required=True)