from odoo import fields, models ,api
from odoo.exceptions import ValidationError, UserError

class Reclamacions(models.Model):
    _name = 'reclamacions'
    _description = 'Reclamacions'
    

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
    closing_reason_id = fields.Many2one('closing.reason', string='Motiu de Tancament o Cancel·lació')
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


    # Métodos para manejar transiciones de estado
    def action_open(self):
        self.ensure_one()
        if self.state == 'new':
            self.state = 'in_progress'
        else:
            raise UserError("Només es pot obrir una reclamació que està en estat 'nova'.")

    def action_close(self):
        self.ensure_one()
        if self.state not in ['closed', 'cancelled']:
            self.state = 'closed'
        else:
            raise UserError("No es pot tancar una reclamació que està tancada o cancel·lada.")

    def action_cancel(self):
        self.ensure_one()
        if self.state not in ['closed', 'cancelled']:
            self.state = 'cancelled'
        else:
            raise UserError("No es pot cancel·lar una reclamació que està tancada o cancel·lada.")

    def action_reopen(self):
        self.ensure_one()
        if self.state == 'closed':
            self.state = 'in_progress'
        else:
            raise UserError("Només es pot reobrir una reclamació tancada.")

    @api.model
    def create(self, vals):
        if 'sale_order_id' in vals:
            existing_complaint = self.search([('sale_order_id', '=', vals['sale_order_id']), ('state', '!=', 'cancelled'), ('state', '!=', 'closed')])
            if existing_complaint:
                raise ValidationError("Ja existeix una reclamació oberta per aquesta comanda.")
        return super(Reclamacions, self).create(vals)

    def action_open(self):
        self.status = 'open'

    @api.depends('sale_order_id')
    def _compute_invoice_count(self):
        for record in self:
            invoices = self.env['account.move'].search([('sale_order_id', '=', record.sale_order_id.id), ('move_type', '=', 'out_invoice')])
            record.invoice_count = len(invoices)

    @api.depends('sale_order_id')
    def _compute_picking_count(self):
        for record in self:
            pickings = self.env['stock.picking'].search([('sale_id', '=', record.sale_order_id.id)])
            record.picking_count = len(pickings)
