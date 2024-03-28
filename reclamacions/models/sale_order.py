from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def action_cancel(self):
        # Asegurarse de ejecutar la lógica original de cancelación
        res = super(SaleOrder, self).action_cancel()

        # Cancelar facturas asociadas no publicadas
        invoices_to_cancel = self.invoice_ids.filtered(lambda inv: inv.state != 'posted')
        invoices_to_cancel.button_draft()
        invoices_to_cancel.button_cancel()

        # Cancelar envíos asociados no realizados
        pickings_to_cancel = self.picking_ids.filtered(lambda pick: pick.state not in ['done', 'cancel'])
        pickings_to_cancel.action_cancel()

        # Enviar correo al cliente sobre la cancelación
        template = self.env.ref('views.email_template_sale_order_cancelled')
        for order in self:
            template.sudo().send_mail(order.id, force_send=True)

        return res
