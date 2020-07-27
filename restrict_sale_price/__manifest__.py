{
    'name': 'Restrict Sale Price',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'summary': 'In the sale order form of order lines fields restrictions',
    'author': 'Oodu Implementers Private Limited',
    'license': 'OPL-1',
    'website': 'https://www.odooimplementers.com',
    'description': 'This module allows to In the sale order form of order lines fields restrictions',
    'depends': ['sale_management'],
    'data': [
        'views/sale_views.xml',
        'security/sale_group.xml',
    ],
    'images': ['static/description/icon.png'],
    'auto_install': False,
    'installable': True,
    'application': False,
}