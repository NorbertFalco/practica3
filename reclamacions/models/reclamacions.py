from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class Reclamacions(models.Model):
    _name = 'reclamacions'
    _description = 'Reclamacions'

    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date', default=fields.Date.today())
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string='Status', default='draft')


    def action_open(self):
        self.status = 'open'
