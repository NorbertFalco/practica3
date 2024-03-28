from odoo import fields, models ,api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger('reclamacions')

class Reclamacions(models.Model):
    _name = 'reclamacions'
    _description = 'Reclamacions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    # el títol de la reclamació
    title = fields.Char(string='Title', required=True)
    
    # el client que fa la reclamació
    # client_id = fields.Many2one('res.partner', string='Client', required=True)
    customer_name = fields.Char(compute='_compute_customer_name', string='Cliente', store=True)
    
    # l'usuari que crea, modifica i tanca la reclamació
    user_id = fields.Many2one('res.users', string='Usuari', default=lambda self: self.env.user)
    
    # la data de creació, modificació i tancament de la reclamació
    creation_date = fields.Date(string='Data de creació', default=fields.Date.today())
    edit_date = fields.Date(string='Data de modificació')
    closing_date = fields.Date(string='Data de tancament')
    
    # la comanda de venda associada a la reclamació
    sale_order_id = fields.Many2one('sale.order', string='Comanda de venda', required=True)

    sale_order_selection = fields.Selection(
        selection=lambda self: self._get_sale_order_selection(),
        string='Comanda de venda'
    )


    @api.model
    def _get_sale_order_selection(self):
        sale_orders = self.env['sale.order'].search([])
        return [(order.id, order.name) for order in sale_orders]


    @api.constrains('sale_order_id', 'state')
    def _check_unique_reclamacio(self):
        for reclamacio in self:
            existing_open_reclamacions = self.search([
                ('sale_order_id', '=', reclamacio.sale_order_id.id),
                ('state', 'in', ['new', 'in_progress']),
                ('id', '!=', reclamacio.id)
            ])
            if existing_open_reclamacions:
                raise ValidationError("Ja existeix una reclamació oberta per a aquesta comanda.")


    # la descripció de la reclamació
    ticket_description = fields.Text(string='Descripció de la reclamació') 

    # el nombre de factures i enviaments associats a la comanda
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Nombre de Factures')

    # el nombre d'enviaments associats a la comanda
    delivery_count = fields.Integer(compute='_compute_delivery_count', string='Nombre d\'Enviaments')
    picking_count = fields.Integer(compute='_compute_picking_count', string='Nombre d\'Enviaments')


    # l'estat de la reclamació
    state = fields.Selection([
        ('new', 'Nova'),
        ('in_progress', 'En Tractament'),
        ('closed', 'Tancada'),
        ('cancelled', 'Cancel·lada')
    ], string='State', default='new', required=True, copy=False, tracking=True)

    # la resolució de la reclamació
    resolution_description = fields.Text(string='Descripció de la resolució')

    # els missatges associats a la reclamació
    missatges_ids = fields.One2many('missatges', 'reclamacio_id', string='Missatges')

    motiu_id = fields.Many2one('motiu', string='Motiu de Tancament', readonly=True)
    motiu_name = fields.Char(string='Motiu de Tancament', readonly=True)



    @api.depends('sale_order_id')
    def _compute_customer_name(self):
        for rec in self:
            rec.customer_name = rec.sale_order_id.partner_id.name if rec.sale_order_id else ''


    def action_close(self):
        self.ensure_one()
        if self.state not in ['closed', 'cancelled']:
            self.closing_date = fields.Date.today() 
            self.state = 'closed'
            # Devuelve una acción para abrir la vista del motivo de cierre
            return {
                'type': 'ir.actions.act_window',
                'name': 'Seleccionar Motiu',
                'res_model': 'motiu',
                'view_mode': 'form',
                'view_id': self.env.ref("reclamacions.view_motiu_form").id,
                'context': {
                                'default_reclamacio_id': self.id,
                            },                
                'target': 'new',
        }

    def action_cancel(self):
        self.ensure_one()
        if self.state not in ['closed', 'cancelled']:
            self.state = 'cancelled'
            return {
                        'type': 'ir.actions.act_window',
                        'name': 'Motiu',
                        'res_model': 'motiu',
                        'view_mode': 'form',
                        'view_id': self.env.ref("reclamacions.view_motiu_form").id,
                        'context': {'default_reclamacio_id': self.id},
                        'target': 'new',
                    }


    @api.model
    def create(self, vals):
    # Comprueba si hay una reclamación existente con el mismo 'sale_order_id' que no esté cancelada o cerrada    
        existing_open_reclamacio = self.search([
        ('sale_order_id', '=', vals.get('sale_order_id')),
        ('state', '=', 'open')
    ])
        if existing_open_reclamacio:
            raise ValidationError("Ya existe una reclamación abierta para esta comanda.")

    # Si pasa las validaciones, crea la reclamación
        return super(Reclamacions, self).create(vals)



    def action_cancel_sale_order(self):
        if self.sale_order_id:
            try:
                self.sale_order_id._action_cancel()
                self.action_cancel()
                return {
                'type': 'ir.actions.act_window',
                'name': 'Motiu',
                'res_model': 'motiu',
                'view_mode': 'form',
                'view_id': self.env.ref("reclamacions.view_motiu_form").id,
                'context': {'default_reclamacio_id': self.id},  # Pasar el ID de la reclamación
                'target': 'new',
            }
            except UserError as e:
                raise UserError("Error al cancelar la venta: %s" % str(e))
        else:
            raise UserError("La reclamació no està associada a cap comanda de venta.")



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

    @api.onchange('missatges_ids')
    def _onchange_missatges_ids(self):
        if any(missatge.reclamacio_id.state == 'new' for missatge in self.missatges_ids):
            self.state = 'in_progress'

    def write(self, vals):
            if vals:
                vals['edit_date'] = fields.Date.today()
            return super(Reclamacions, self).write(vals)




