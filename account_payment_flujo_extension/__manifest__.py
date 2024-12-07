{
    'name': 'Account Payment Flujo Extension',
    'summary': 'Extension to add mpflujo and mpgrupo_flujo fields to payments',
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'category': 'Accounting',
    'license': 'LGPL-3',
    'version': '17.0.0.0.1',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_views.xml',
        'views/account_batch_payment_views.xml',
        'views/account_move_views.xml',  
        'views/account_move_line_views.xml',  
    ],
    'installable': True,
    'application': False,
}
