from odoo import fields, models ,api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger('reclamacions')

class venda(models.Model):
    _inherit = 'sale.order'


    reclamacions_ids = fields.One2many('reclamacions', 'sale_order_id', string='Reclamaciones')


    
