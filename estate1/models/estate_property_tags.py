from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"

    
    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="color")

