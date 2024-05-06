from odoo import fields, models, tools

class CustomSalesReport(models.Model):
    _name = 'custom.sales.report'
    _description = 'Custom Sales Report'
    _auto = False

    salesperson = fields.Many2one('res.users', 'Comercial', readonly=True)
    
    status = fields.Selection([
        ('draft', 'Pressupost'),
        ('sent', 'Pressupost Enviat'),
        ('sale', 'Comanda de Vendes'),
        ('done', 'Finalitzat'),
        ('cancel', 'Cancel·lat')
    ], string='Estat de la comanda', readonly=True)

    order_count = fields.Integer('Nombre de comandes', readonly=True)

    total_cost = fields.Float('Import total', readonly=True)


    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'custom_sales_report')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW custom_sales_report AS (
                SELECT
                    MIN(so.id) AS id,
                    so.user_id AS salesperson,
                    so.state AS status,
                    COUNT(*) AS order_count,
                    SUM(so.amount_total) AS total_cost
                FROM
                    sale_order so
                GROUP BY
                    so.user_id,
                    so.state
            )
        """)


    def action_custom_sales_report_print(self):
        """ This method triggers the report printing for the selected records. """
        # Retrieve the report action reference to call it
        report_action = self.env.ref('practica4.action_custom_sales_report_print')
        
        # Retrieve the record IDs from the context to pass them to the report action
        record_ids = self.env.context.get('active_ids', False)
        
        # Debugging: Print the record IDs and ensure they are as expected
        print(f"Record IDs: {record_ids}")
        
        # Call the report action and pass the record IDs
        report_result = report_action.report_action(record_ids)
        
        # Debugging: Print the report result to check what data is being passed to the template
        print(f"Report action result: {report_result}")
        
        # Return the result of the report action
        return report_result




