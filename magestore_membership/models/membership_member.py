# -*- coding: utf-8 -*-
from odoo import models, fields, api

class membership_products(models.Model):
    _name = 'membership.member'

    # product_id = fields.Many2Many('product.template', 'product_template', 'id', string="Product id matching")
    # package_id = fields.Many2one('membership.package', string='Package', required=True, ondelete='cascade')
    # partner_id = fields.Many2one('res.partner', string='Partner', ondelete='cascade', index=True)
    package_id = fields.Integer(string='Package')
    partner_id = fields.Integer(string='Partner')
    membership_start = fields.Date(string='Membership Start')
    membership_stop = fields.Date(string='Membership Stop')
    membership_status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive'), ('cancel', 'Cancel')], string='Membership Status', default='active')
    discount = fields.Float(string='Discount')