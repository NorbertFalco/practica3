{
    "name": "Reclamacions",
    "version": "16.0.0",
    "application": True,
    "depends": ["base", "mail", "sale", 'account', 'stock'],
    "data": [
        'security/ir.model.access.csv',
        'views/closing_reason_views.xml',
        'views/email_template_order_cancellation.xml',
        'views/formulari_reclamacions.xml',
        'views/llista_reclamacions_views.xml',
        'views/motiu_cancelar.xml',
        'views/motiu.xml',
        'views/reclamacions_menu.xml',
        'views/venda_views.xml',

        
    ],
    "installable": True,
    'license': 'LGPL-3',
}
