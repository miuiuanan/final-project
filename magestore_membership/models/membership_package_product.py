# -* coding: utf-8 -*-
from odoo import models, fields, api

# class MembershipPackageProduct(models.Model):
#     _name = 'membership.package_product'
#     _table = 'membership_package_product'
#     discount = fields.Float(string='Discount')
    # id = fields.Integer()

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    discount_to = fields.Selection([('all', 'All products'), ('specific', 'Specific Products')], default='all')
    package_product_ids = fields.Many2many('product.product', 'membership_package_product', 'package_id', 'product_id', string='Product Select')