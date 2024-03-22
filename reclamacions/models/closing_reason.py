from odoo import models, fields, api

class ClosingReason(models.Model):
    _name = 'closing.reason'
    _description = 'Motiu de Tancament'

    name = fields.Char('Motiu', required=True)
    description = fields.Text('Descripció')

    def action_reopen_ticket(self):
        # Lógica para reabrir el ticket
        self.ensure_one()
        if self.state == 'closed':
            self.state = 'open'
        # ... más lógica si es necesario ...
