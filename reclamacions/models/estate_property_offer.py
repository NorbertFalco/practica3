from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Model per estate.property.offer'

    price = fields.Float('Preu')
    status = fields.Selection([
        ('accepted', 'Acceptada'),
        ('refused', 'Refusada'),
        ('pending', 'En tractament')
    ], string='Status', default='pending', copy=False)
    partner_id = fields.Many2one('res.partner', string='Comprador', required=True, copy=False)
    property_id = fields.Many2one('estate.property', string='Propietat', required=True, copy=False)
    date = fields.Date(string='Offer Date', default=fields.Date.context_today, copy=False)
    validity = fields.Integer(string='Validity (days)', default=7)
    is_best_offer = fields.Boolean(string='Is Best Offer', compute='_compute_is_best_offer', store=True)

    @api.depends('property_id.offer_ids', 'price')
    def _compute_is_best_offer(self):
        for offer in self:
            max_price = max(offer.property_id.offer_ids.mapped('price'), default=0)
            offer.is_best_offer = offer.price == max_price

    @api.model
    def create(self, vals):
        result = super(EstatePropertyOffer, self).create(vals)
        # Actualitza el preu de venda i el comprador de la propietat si l'estat de l'oferta és 'accepted'
        if result.status == 'accepted':
            result.property_id.write({
                'selling_price': result.price,
                'buyer_id': result.partner_id.id,
                'expected_selling_price': result.price  # Actualitzem també el preu de venda esperat
            })
        return result

    def write(self, vals):
        result = super(EstatePropertyOffer, self).write(vals)
        if 'status' in vals and vals['status'] == 'accepted':
            for record in self:
                # Assegura que només s'actualitza si és l'oferta acceptada més recent
                if record.status == 'accepted':
                    record.property_id.write({
                        'selling_price': record.price,
                        'buyer_id': record.partner_id.id,
                        'expected_selling_price': record.price  # Actualitzem també el preu de venda esperat
                    })
        return result

    def _update_property_on_offer_accepted(self, record):
        if record.status == 'accepted':
            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id),
                ('status', '=', 'accepted'),
            ])
            if other_offers:
                other_offers.write({'status': 'refused'})
            record.property_id.write({
                'selling_price': record.price,
                'expected_selling_price': record.price,  # Aquesta línia s'ha afegit per actualitzar el preu de venda esperat
                'buyer_id': record.partner_id.id,
                'state': 'offer_accepted',
            })
