{
    "name": "Reclamacions",
    "version": "16.0.0",
    "application": True,
    "depends": ["base", "mail", "sale", 'account', 'stock'],
    "data": [
        'security/ir.model.access.csv',
        'views/llista_reclamacions_views.xml',
        'views/reclamacions_menu.xml',
        'views/formulari_reclamacions.xml',
        'views/motiu.xml',
        'views/closing_reason_views.xml',
        'views/venda_views.xml',
        'views/email_template_order_cancellation.xml'
    ],
    "installable": True,
    'license': 'LGPL-3',
}
