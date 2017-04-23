# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Membership Kidzplay',
    'version': '1.0',
    'category': 'Sales',
    'description': """Kidzplay""",
    'depends': ['base', 'product', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/membership_invoice_views.xml',
        'data/membership_data.xml',
        'views/product_views.xml',
        'views/partner_views.xml',
        'report/report_membership_views.xml',
    ],
    'demo': [
        'data/membership_demo.xml',
    ],
    'website': 'https://www.odoo.com/page/community-builder',
    'test': [
        '../account/test/account_minimal_test.xml',
    ],
    'installable': True,
    'application': True,
}
