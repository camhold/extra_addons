{
    'name': 'Stock Location Code',
    'license': 'LGPL-3',
    'version': '17.0.0.0.1',
    'category': 'Warehouse',
    'summary': 'Adds a unique alphanumeric code to stock locations',
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'depends': ['stock'],
    'data': [
        'views/stock_location_views.xml',
        'data/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
