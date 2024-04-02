from odoo import fields, models, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class Motiu(models.Model):
    _name = 'motiu'
    _description = 'Motiu de tancament'

    reclamacio_id = fields.Many2one('reclamacions', string='Reclamació', required=True)
    motiu_closing_reason = fields.Many2one('closing.reason', string='Motiu', required=True)
    motiu_name = fields.Char(related='motiu_closing_reason.name', string='Motiu de Tancament')

    def confirm_motiu(self):
        for rec in self:
            rec.reclamacio_id.motiu_id = rec.motiu_closing_reason.id
            rec.reclamacio_id.motiu_name = rec.motiu_closing_reason.name