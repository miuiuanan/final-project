# -*- coding: utf-8 -*-
from odoo import models, fields, api
import time
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[('membership', 'Membership')])
    price = fields.Integer(string='Membership Price', help='Set membership pricing')
    discount = fields.Float(string='Membership Discount')
    duration = fields.Integer(string='Membership Package Expired')
    discount_type = fields.Selection([('percent', 'Percentage'), ('fixed', 'Fixed')], string='Discount Type', default='percent')

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if self.type == 'membership':
            print self.id
            time.sleep(10)
            self.env['membership.package'].create({
                'product_id': self.id,
                'duration': self.duration,
                'discount': self.discount,
                'name': self.name,
                'discount_type': self.discount_type,
                'discount_to': self.discount_to
            })
        return res

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if self.type == 'membership':
            MembershipPackage = self.env['membership.package'].search([
                ('product_id', '=', int(self.id))
            ], limit=1)
            if MembershipPackage.id:
                self.env['membership.package'].browse(int(MembershipPackage.id)).write({
                    'product_id': self.id,
                    'duration': self.duration,
                    'discount': self.discount,
                    'name': self.name,
                    'discount_type': self.discount_type,
                    'discount_to': self.discount_to
                })
            if MembershipPackage.id == False:
                self.env['membership.package'].create({
                    'product_id': self.id,
                    'duration': self.duration,
                    'discount': self.discount,
                    'name': self.name,
                    'discount_type': self.discount_type,
                    'discount_to': self.discount_to
                })
        if self.type != 'membership':
            MembershipPackage = self.env['membership.package'].search([
                ('product_id', '=', int(self.id))
            ], limit=1)
            if MembershipPackage.id:
                self.env['membership.package'].browse(int(MembershipPackage.id)).unlink()
        return res