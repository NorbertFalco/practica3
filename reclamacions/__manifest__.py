{
    "name": "Reclamacions",
    "version": "16.0.0",
    "application": True,
<<<<<<< HEAD
    "depends": ["base", "mail", "sale", 'account', 'stock'],
=======
    "depends": ["base", "mail", "sale", "account"],
>>>>>>> ad4bb88 (factura id es mostra al cancelar i confirmem la factura desde la comanda de venda)
    "data": [
        'security/ir.model.access.csv',
        'views/llista_reclamacions_views.xml',
        'views/reclamacions_menu.xml',
        'views/formulari_reclamacions.xml',
        'views/motiu.xml',
        'views/closing_reason_views.xml',
        'views/venda_views.xml',
<<<<<<< HEAD
        'views/email_template_order_cancellation.xml'
        
=======
        'views/motiu_cancelar.xml',
>>>>>>> ad4bb88 (factura id es mostra al cancelar i confirmem la factura desde la comanda de venda)
    ],
    "installable": True,
    'license': 'LGPL-3',
}
