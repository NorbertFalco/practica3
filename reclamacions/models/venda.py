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

            # Aquí se incluye tu método action_cancel personalizado
    def action_cancel(self):
        # Comprobar si hay facturas publicadas asociadas a la orden
        published_invoices = self.invoice_ids.filtered(lambda inv: inv.state == 'posted')
        if published_invoices:
            raise UserError(_('No es pot cancel·lar lordre perquè hi ha factures publicades associades.'))

        # Asegurarse de ejecutar la lógica original de cancelación
        res = super(venda, self).action_cancel()

        # Cancelar facturas asociadas no publicadas
        invoices_to_cancel = self.invoice_ids.filtered(lambda inv: inv.state != 'posted')
        for invoice in invoices_to_cancel:
            invoice.action_invoice_draft()
            invoice.button_cancel()

        # Cancelar envíos asociados no realizados
        pickings_to_cancel = self.picking_ids.filtered(lambda pick: pick.state not in ['done', 'cancel'])
        pickings_to_cancel.action_cancel()

        # Enviar correo al cliente sobre la cancelación
        template = self.env.ref('reclamacions.email_template_order_cancellation')

        for order in self:
            template.send_mail(order.id, force_send=True)
            order.message_post(body=("Correu de cancel·lació enviat al client."))

        return res