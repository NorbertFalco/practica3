{
    "name": "Practica 4",
    "version": "16.0.0",
    "application": True,
    "depends": ["base", "mail", "sale", 'account', 'stock'],
    "data": [
        'security/ir.model.access.csv',
        'views/practica4_view.xml',
        'report/practica4_report.xml',
        'views/sale_menu.xml',
        'report/custom_sales_report_template.xml',
    ],
    "installable": True,
    'license': 'LGPL-3',
}

