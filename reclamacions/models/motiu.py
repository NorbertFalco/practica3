from odoo import fields, models, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class Motiu(models.Model):
    _name = 'motiu'
    _description = 'Motiu de tancament'

    motiu_id = fields.Many2one('closing.reason', string='Motiu')