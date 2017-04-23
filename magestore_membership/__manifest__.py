# -*- coding: utf-8 -*-
{
    'name': 'Magestore Membership',
    'summary': """Magestore Membership Module""",
    'description': """For multipurpose membership management""",
    'author': 'Magestore',
    'website': 'http://www.magestore.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/membership_views.xml',
        'views/partner_views.xml',
        'views/product_views.xml',
    ],
    
    'installable': True,
    'application': True,
}