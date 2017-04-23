# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MembershipPackage(models.Model):
    _name = 'membership.package'

    # product_id = fields.Many2Many('product.template', 'product_template', 'id', string="Product id matching")
    product_id = fields.Integer(string='Product ID')
    duration = fields.Integer(string="Membership Duration")
    discount = fields.Float(string="Membership Discount")
    discount_type = fields.Selection([('fixed', 'Fixed'), ('percent', 'Percent')], default='percent')
    name = fields.Char(string='Name')
    discount_to = fields.Selection([('all', 'All products'), ('specific', 'Specific Products')], default='all')