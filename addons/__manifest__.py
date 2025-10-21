{
    'name': 'Purchase Process Management',
    'version': '18.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Gestion du processus d\'achat pour entreprise de construction',
    'description': """
        Module de gestion du processus d'achat selon la documentation
        - Gestion des projets et chantiers
        - Processus de demande d'achat
        - Workflow de validation
        - Tableaux de bord
        - Réception et contrôle
    """,
    'author': 'Votre Entreprise',
    'website': 'https://www.votre-entreprise.com',
    'depends': ['base', 'purchase', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/project_views.xml',
        'views/chantier_views.xml',
        'views/demande_achat_views.xml',
        'views/menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
