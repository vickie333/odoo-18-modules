from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "sequence, name"

    name = fields.Char(string='Type Name', required=True, tracking=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(string='Sequence', default=1, help="Used to order types in the user interface.")
    offer_ids = fields.One2many(related="property_ids.offer_ids", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    # _sql_constraints = [
    #     ('unique_type_name', 'UNIQUE(name)', 'The type name must be unique.')
    # ]

    @api.constrains('name')
    def _check_name(self):
        for type in self:
            if not type.name:
                raise ValidationError("The type name must be set.")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)