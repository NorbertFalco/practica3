from odoo import fields, models ,api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger('reclamacions')

class venda(models.Model):
    _inherit = 'sale.order'

    reclamacions_ids = fields.One2many('reclamacions', 'sale_order_id', string='Reclamaciones')
    invoice_id = fields.Many2one('account.move', string='Factura', compute='_compute_invoice_id', store=True)

    @api.depends('invoice_ids')
    def _compute_invoice_id(self):
        for order in self:
            if order.invoice_ids:
                # Seleccionar la primera factura de la lista de facturas asociadas
                order.invoice_id = order.invoice_ids[0].id
            else:
                order.invoice_id = False
                
    def action_confirm_invoice(self):
        
        for order in self:
            if not order.invoice_ids:
                raise UserError("No hay ninguna factura para confirmar en esta orden.")

            for invoice in order.invoice_ids:
                if invoice.state != 'draft':
                    raise UserError("La factura no está en estado de borrador para confirmar.")

                # Confirmar la factura utilizando action_post() del modelo account.move
                invoice.action_post()

                # Guardar el valor de la primera factura en invoice_id de la orden de venta
                order.invoice_id = invoice

                _logger.info("Factura confirmada para la orden de venta: %s", order.name)

        return True