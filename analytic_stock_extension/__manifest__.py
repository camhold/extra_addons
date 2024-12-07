{
    'name': 'Stock Analytic Extension',
    'category': 'Warehouse',
    'license': 'LGPL-3',
    'version': '17.0.0.0.1',
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'depends': ['stock', 'account', 'analytic','analytic_account_blocker'],
    'data': [
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
}
