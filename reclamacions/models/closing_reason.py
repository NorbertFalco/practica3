from odoo import models, fields, api

class ClosingReason(models.Model):
    _name = 'closing.reason'
    _description = 'Motiu de Tancament'

    name = fields.Char('Motiu', required=True)
    description = fields.Text('Descripció')
    state = fields .Selection([
        ('new', 'Nou'),
        ('in_progress', 'En progress'),
        ('closed', 'Tancat'),
        ('cancelled', 'Cancel·lat')
    ], default='new', string='Estat', required=True, copy=False, tracking=True)
    



    def action_reopen_ticket(self):
        # Lógica para reabrir el ticket
        self.ensure_one()
        if self.state == 'closed':
            self.state = 'open'
        # ... más lógica si es necesario ...
        

    @api.onchange('name')
    def onchange_name(self):
        if self.motiu_ids:
            for motiu in self.motiu_ids:
                motiu.motiu_closing_reason = self.id    

   