from odoo import fields, models ,api
from odoo.exceptions import ValidationError, UserError

class Reclamacions(models.Model):
    _name = 'reclamacions'
    _description = 'Reclamacions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    title = fields.Char(string='Títol', required=True)
    customer_name = fields.Char(compute='_compute_customer_name', string='Cliente', store=True)
    description = fields.Text(string='Descripció')
    date = fields.Date(string='Data', default=fields.Date.today())
    user_id = fields.Many2one('res.users', string='Usuari', default=lambda self: self.env.user)
    status = fields.Selection([
        ('draft', 'Esborrany'),
        ('open', 'Obert'),
        ('closed', 'Tancat'),
    ], string='Estat', default='draft')
    missatges_ids = fields.One2many('missatges', 'reclamacio_id', string='Missatges')
    sale_order_id = fields.Many2one('sale.order', string='Comanda de Vendes Associada')
    resolution_description = fields.Text('Descripció de la Resolució Final')

    state = fields.Selection([
        ('new', 'Nova'),
        ('in_progress', 'En Tractament'),
        ('closed', 'Tancada'),
        ('cancelled', 'Cancel·lada')
    ], string='Estat', default='new')
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Nombre de Factures')
    picking_count = fields.Integer(compute='_compute_picking_count', string='Nombre d\'Enviaments')
    sale_order_id = fields.Many2one('sale.order', string='Comanda de Vendes')
    resolution = fields.Text(string='Resolució')
    closing_reason_id = fields.Many2one('closing.reason', string='Motiu de Tancament')
# ... tus campos y métodos existentes ...


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
