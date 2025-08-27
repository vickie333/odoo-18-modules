from odoo import models, fields

class EstateImage(models.Model):
    _name = 'estate.image'
    _description = 'Estate Image'
    _order = 'sequence, id'

    name = fields.Char(string='Name',required=True)
    description = fields.Text(string='Description')
    image = fields.Binary(string='Image',required=True)
    estate_id = fields.Many2one('estate.estate',string='Estate')
    sequence = fields.Integer(string='Sequence',default=10)
    image_type = fields.Selection(
        [('exterior','Exterior'),('interior','Interior'),('floorplan','Floorplan'),('other','Other')],
        string='Image Type',default='interior')