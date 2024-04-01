from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class Missatges(models.Model):
    _name = 'missatges'
    _description = 'Missatges de reclamacions'

    text = fields.Text(string='Missatge', required=True)
    author_id = fields.Reference(selection=[('res.users', 'Usuari'), ('res.partner', 'Client')], string='Autor', required=True, help="Autor del missatge")
    date = fields.Datetime(string='Data', default=fields.Datetime.now, readonly=True)
    reclamacio_id = fields.Many2one('reclamacions', string='Reclamació', required=True)

    def unlink(self):
        raise ValidationError("No es poden esborrar els missatges.")

    def write(self, vals):
        raise ValidationError("No es poden modificar els missatges.")

    @api.model
    def action_send_message(self, reclamacio_id, text):
        # Create a new message associated with the given reclamacion ID
        reclamacion = self.env['reclamacions'].browse(reclamacio_id)
        new_message = self.create({
            'text': text,
            'author_id': ('res.users', self.env.user.id),
            'reclamacio_id': reclamacion.id
        })
        return new_message