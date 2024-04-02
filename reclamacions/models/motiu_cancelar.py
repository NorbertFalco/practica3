from odoo import fields, models, api
from odoo.exceptions import UserError

class MotiuCancelar(models.Model):
    _name = 'motiu.cancelar'  
    _description = 'Motiu de tancament'

    reclamacio_id = fields.Many2one('reclamacions', string='Reclamación', required=True)
    motiu_closing_reason = fields.Many2one('closing.reason', string='Motiu', required=True)
    motiu_name = fields.Char(related='motiu_closing_reason.name', string='Motiu de Tancament')
    sale_order_id = fields.Many2one('sale.order', string='Comanda de venta')
    
    invoice_id = fields.Many2one('account.move', string='Factura', compute='_compute_invoice_id', store=True)
    

    @api.depends('motiu_closing_reason')
    def _compute_invoice_id(self):
        for record in self:
            if record.sale_order_id:
                # Obtener la factura relacionada con la orden de venta
                invoice = record.sale_order_id.invoice_ids.filtered(lambda inv: inv.state != 'cancel')
                record.invoice_id = invoice and invoice[0].id or False
       


    def confirm_motiu(self):
        for rec in self:
            rec.reclamacio_id.motiu_id = rec.motiu_closing_reason.id
            rec.reclamacio_id.motiu_name = rec.motiu_closing_reason.name




                         