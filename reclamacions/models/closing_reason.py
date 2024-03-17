from odoo import models, fields

class ClosingReason(models.Model):
    _name = 'closing.reason'
    _description = 'Motiu de Tancament'

    name = fields.Char('Motiu', required=True)
    description = fields.Text('Descripció')
