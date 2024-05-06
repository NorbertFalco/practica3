from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class practica4(models.Model):
    _inherit = 'sale.order'
    
    total_articles = fields.Integer(string='Total Articles', compute='_compute_total_articles')
    preferred_email = fields.Char(string='Preferred Email')

    def _compute_total_articles(self):
        for order in self:
            # Utilitza un set per a guardar els ids dels productes, així no es poden repetir
            distinct_product_ids = {line.product_id.id for line in order.order_line}
            # El total d'articles és la longitud del set
            order.total_articles = len(distinct_product_ids)

    
    @api.constrains('preferred_email')
    def _check_email(self):
        email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        for record in self:
            if record.preferred_email and not email_regex.match(record.preferred_email):
                raise ValidationError("Si us plau introdueix un email vàlid.")




