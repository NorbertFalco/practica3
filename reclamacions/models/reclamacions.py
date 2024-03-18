from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class Reclamacions(models.Model):
    _name = 'reclamacions'
    _description = 'Reclamacions'

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
    
