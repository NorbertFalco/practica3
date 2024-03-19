{
    "name": "Reclamacions",  # The name that will appear in the App list
    "version": "16.0.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base", "mail", "sale"],  # dependencies
    "data": [
        'security/ir.model.access.csv',
        'views/reclamacions_views.xml',
        'views/reclamacions_menu.xml',
        'views/closing_reason_views.xml',
        'views/motiu.xml',
        
        
        
    ],
    "installable": True,
    'license': 'LGPL-3',
}
