{
    "name": "Reclamacions",  # The name that will appear in the App list
    "version": "16.0.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        'security/ir.model.access.csv',
        'views/reclamacions_views.xml',
        'views/reclamacions_menu.xml',
        
    ],
    "installable": True,
    'license': 'LGPL-3',
}
