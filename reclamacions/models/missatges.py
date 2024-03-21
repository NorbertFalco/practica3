from odoo import fields, models, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class Missatges(models.Model):
    _name = 'missatges'
    _description = 'Missatges de reclamacions'

    text = fields.Text(string='Missatge', required=True)
    author_id = fields.Reference(selection=[('res.users', 'Usuari'), ('res.partner', 'Client')], string='Autor', required=True, help="Autor del missatge")
    date = fields.Datetime(string='Data', default=fields.Datetime.now, readonly=True)
    reclamacio_id = fields.Many2one('reclamacions', string='Reclamació', required=True)
    date_availability = fields.Date(default=fields.Date.today()+relativedelta(months=3),
    copy=False)
    buyer_id = fields.Many2one('res.partner', string='Comprador')
    salesperson_id = fields.Many2one('res.users', string='Comercial')

    @api.model
    def create(self, vals):
        if 'date' not in vals or not vals['date']:
            vals['date'] = fields.Datetime.now()
        return super(Missatges, self).create(vals)

    def write(self, vals):
        raise ValidationError("No es poden modificar els missatges.")

    def unlink(self):
        raise ValidationError("No es poden esborrar els missatges.")
