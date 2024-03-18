from odoo import fields, models ,api
from odoo.exceptions import ValidationError, UserError

class Reclamacions(models.Model):
    _name = 'reclamacions'
    _description = 'Reclamacions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    # el títol de la reclamació
    title = fields.Char(string='Title', required=True)
    
    # el client que fa la reclamació
    client_id = fields.Many2one('res.partner', string='Client', required=True)
    
    # l'usuari que crea, modifica i tanca la reclamació
    user_id = fields.Many2one('res.users', string='Usuari', default=lambda self: self.env.user)
    
    # la data de creació, modificació i tancament de la reclamació
    creation_date = fields.Date(string='Data de creació', default=fields.Date.today())
    edit_date = fields.Date(string='Data de modificació', default=fields.Date.today())
    closing_date = fields.Date(string='Data de tancament', default=fields.Date.today())
    
    # la comanda de venda associada a la reclamació
    sale_order_id = fields.Many2one('sale.order', string='Comanda de venda')

    # la descripció de la reclamació
    ticket_description = fields.Text(string='Descripció de la reclamació') 

    # el nombre de factures i enviaments associats a la comanda
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Nombre de Factures')
    delivery_count = fields.Integer(compute='_compute_delivery_count', string='Nombre d\'Enviaments')

    # el nombre de factures associades a la comanda
    @api.depends('sale_order_id.invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.sale_order_id.invoice_ids)

    # el nombre d'enviaments associats a la comanda
    @api.depends('sale_order_id.picking_ids')
    def _compute_delivery_count(self):
        for record in self:
            record.delivery_count = len(record.sale_order_id.picking_ids)

    # l'estat de la reclamació
    status = fields.Selection([
        ('nova', 'Nova'),
        ('en_tractament', 'En Tractament'),
        ('tancada', 'Tancada'),
        ('cancellada', 'Cancel·lada')
    ], string='Status', default='draft')

    # la resolució de la reclamació
    resolution_description = fields.Text(string='Descripció de la resolució')

# faltarà decidir quins motius de tancament i cancel·lació volem
    closure_reason = fields.Selection([
        ('reason1', 'Reason 1'),
        ('reason2', 'Reason 2'),
        ('reason3', 'Reason 3')
    ], string='Motiu de tancament')

    cancellation_reason = fields.Selection([
        ('reason1', 'Reason 1'),
        ('reason2', 'Reason 2'),
        ('reason3', 'Reason 3')
    ], string='Motiu de cancel·lació')
    


    @api.depends('sale_order_id')
    def _compute_customer_name(self):
        for rec in self:
            rec.customer_name = rec.sale_order_id.partner_id.name if rec.sale_order_id else ''


    @api.model
    def create(self, vals):
    # Comprueba si hay una reclamación existente con el mismo 'sale_order_id' que no esté cancelada o cerrada
        existing_complaint = self.search([
        ('sale_order_id', '=', vals.get('sale_order_id')),
        ('state', 'not in', ['cancelled', 'closed'])
    ])
        if existing_complaint:
            raise ValidationError("Ja existeix una reclamació oberta per aquesta comanda.")

    # Alternativamente, si quieres asegurarte de que no hay reclamaciones en estado 'open',
    # puedes agregar esta condición adicional:
        existing_open_reclamacio = self.search([
        ('sale_order_id', '=', vals.get('sale_order_id')),
        ('state', '=', 'open')
    ])
        if existing_open_reclamacio:
            raise ValidationError("Ya existe una reclamación abierta para esta comanda.")

    # Si pasa las validaciones, crea la reclamación
        return super(Reclamacions, self).create(vals)

    def action_open(self):
        self.ensure_one()
        if self.state == 'new':
            self.state = 'in_progress'
        elif self.state == 'closed':
            self.state = 'in_progress'
        else:
            raise UserError("La reclamación no se puede abrir desde su estado actual.")

    def action_close(self):
        self.ensure_one()
        if self.state not in ['closed', 'cancelled']:
            self.state = 'closed'
        else:
            raise UserError("No se puede cerrar una reclamación que está cerrada o cancelada.")

    def action_cancel(self):
        self.ensure_one()
        if self.state not in ['closed', 'cancelled']:
            self.state = 'cancelled'
        else:
            raise UserError("No se puede cancelar una reclamación que está cerrada o cancelada.")

    def action_reopen(self):
        self.ensure_one()
        if self.state == 'closed':
            self.state = 'in_progress'
        else:
            raise UserError("Solo se puede reabrir una reclamación cerrada.")

    @api.depends('sale_order_id')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.sale_order_id.invoice_ids)

    @api.depends('sale_order_id')
    def _compute_picking_count(self):
        for record in self:
            record.picking_count = len(record.sale_order_id.picking_ids)




