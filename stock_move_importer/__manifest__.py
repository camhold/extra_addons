{
    'name': 'Stock Picking Importer',
    'license': 'LGPL-3',
    'version': '17.0.0.0.1',
    'depends': ['base', 'stock', 'base_import'],
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'category': 'Warehouse',
    'description': 'Import stock picking records from Excel.',
    'data': [
        'security/ir.model.access.csv',
        'wizards/stock_import_wizard_view.xml',

    ],
}
