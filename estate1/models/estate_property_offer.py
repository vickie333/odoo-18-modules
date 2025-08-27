
from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ("accepted","Accepted"),
        ("refused","Refused")
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline",compute="_compute_date_deadline")
    create_date = fields.Datetime(string="Create Date", default=fields.Datetime.now)
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)

    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date + timedelta(days=offer.validity)

    def action_accept_offer(self):
        for offer in self:
            offer.ensure_one()

            # Validaciones
            if not offer.property_id:
                raise UserError("This offer is not linked to a property.")
            if offer.property_id.state == 'canceled':
                raise UserError("Cannot accept an offer for a canceled property.")

            # 1) comprobar si ya hay otra accepted (antes de aceptar)
            other_accepted = offer.property_id.offer_ids.filtered(
                lambda o: o.status == 'accepted' and o.id != offer.id
            )
            if other_accepted:
                raise UserError("Only one offer can be accepted for a given property.")

            # 2) marcar esta oferta como accepted
            offer.status = 'accepted'

            # 3) actualizar la propiedad
            prop = offer.property_id
            prop.selling_price = offer.price
            prop.buyer_id = offer.partner_id
            prop.state = 'offer_accepted'  

            # 4) rechazar *solo* las otras ofertas (excluyendo la aceptada)
            other_offers = prop.offer_ids.filtered(lambda o: o.id != offer.id and o.status != 'refused')
            if other_offers:
                other_offers.write({'status': 'refused'})
 

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"

    @api.constrains('price')
    def _check_price(self):
        for offer in self:
            if offer.price <= 0:
                raise ValidationError("The offer price must be positive")
            
    @api.model
    def create(self, vals):
        prop = self.env['estate.property'].browse(vals.get('property_id'))

        best = max(prop.offer_ids.mapped('price'), default=0.0)

        if vals.get('price') < best:
            raise UserError("The offer price must be greater than %.2f" % best)

        record = super().create(vals)
    
        record.property_id.write({'state': 'offer_received'})
        return record