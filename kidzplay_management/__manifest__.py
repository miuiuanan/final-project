# -*- coding: utf-8 -*-
{
    'name': "Kidzplay Management",

    'summary': """
        Manage Kidzplay""",

    'description': """
        - POS
        - Membership
    """,

    'author': "Magestore",
    'website': "http://www.magestore.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale','website_sale','website_blog'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/kidzplay_footer.xml',
        'views/kidzplay_copyright.xml',
        'views/kidzplay_block_post_related.xml',
        'data/default_data.xml'
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
}