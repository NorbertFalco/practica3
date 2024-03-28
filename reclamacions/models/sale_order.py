from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Aquí irían otros métodos CRUD sobrescritos o añadidos como _add_precomputed_values, create, etc.

    # Aquí se incluye tu método action_cancel personalizado
    def action_cancel(self):
        # Comprobar si hay facturas publicadas asociadas a la orden
        published_invoices = self.invoice_ids.filtered(lambda inv: inv.state == 'posted')
        if published_invoices:
            raise UserError(_('No se puede cancelar la orden porque existen facturas publicadas asociadas.'))

        # Asegurarse de ejecutar la lógica original de cancelación
        res = super(SaleOrder, self).action_cancel()

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
            order.message_post(body=_("Correo de cancelación enviado al cliente."))

        return res

    # Aquí seguirían otros métodos de negocio sobrescritos o añadidos como _expected_date, compute_uom_qty, etc.

    # No olvides revisar la referencia a tu plantilla de correo electrónico para que coincida con el ID externo correcto.
