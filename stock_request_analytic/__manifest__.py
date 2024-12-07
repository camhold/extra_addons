
{
    'name': 'stock_request_analytic',
    'license': 'LGPL-3',
    'version': '17.0.0.0.1',
    'category': 'Inventory',
    'summary': 'Inherit analytic accounts in stock requests',
    'description': 'Adds analytic account fields to stock requests and their lines.',
    'author': 'Diego Gajardo, Camilo Neira',
    'depends': ['stock_request', 'account'],
    'data': [
        'views/stock_request_views.xml',
    ],
    'installable': True,
    'application': False,
}
