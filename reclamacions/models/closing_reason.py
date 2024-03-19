from odoo import models, fields

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
    



    def action_close_ticket(self):
        # Lógica para cerrar el ticket
        self.ensure_one()
        if self.state not in ['closed', 'cancelled']:
            self.state = 'closed'
        return {
                'type': 'ir.actions.act_window',
                'name': 'Motiu',
                'res_model': 'motiu',
                'view_mode': 'form',
                'view_id': self.env.ref("motiu.view_motiu_form").id,
                'context': {},
                'target': 'new',
            }

    def action_cancel_ticket(self):
        # Lógica para cancelar el ticket
        self.ensure_one()
        if self.state != 'cancelled':
            self.state = 'cancelled'
        # ... más lógica si es necesario ...

    def action_reopen_ticket(self):
        # Lógica para reabrir el ticket
        self.ensure_one()
        if self.state == 'closed':
            self.state = 'open'
        # ... más lógica si es necesario ...

    def action_cancel_sale_order(self):
        # Lógica para cancelar la orden de venta asociada
        self.ensure_one()
        # Aquí tendrás que añadir tu propia lógica para cancelar la orden de venta
        # posiblemente llamando a un método en el modelo 'sale.order'