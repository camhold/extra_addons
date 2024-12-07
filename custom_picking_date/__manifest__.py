{
    'name': 'Custom Picking Date',
    'category': 'Stock',
    'summary': 'Remove readonly restriction on date_done field in stock.picking',
    'description': """
        This module removes the readonly restriction on the date_done field in stock.picking model.
    """,
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'license': 'LGPL-3',
    'version': '17.0.0.0.1',
    'website': 'https://www.holdconet.com',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}
