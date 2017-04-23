# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime
from datetime import timedelta

class Invoice(models.Model):
    _inherit = 'account.invoice'

    # @api.multi
    # def action_cancel_draft(self):
    #     self.env['membership.membership_line'].search([
    #         ('account_invoice_line', 'in', self.mapped('invoice_line_ids').ids)
    #     ]).write({'date_cancel': False})
    #     return super(Invoice, self).action_cancel_draft()
    #
    # @api.multi
    # def action_cancel(self):
    #     '''Create a 'date_cancel' on the membership_line object'''
    #     self.env['membership.membership_line'].search([
    #         ('account_invoice_line', 'in', self.mapped('invoice_line_ids').ids)
    #     ]).write({'date_cancel': fields.Date.today()})
    #     return super(Invoice, self).action_cancel()


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def write(self, vals):
        res = super(AccountInvoiceLine, self).write(vals)
        for line in self.filtered(lambda line: line.invoice_id.type == 'out_invoice'):
            if line.product_id.type == 'membership':
                ProductProduct = self.env['product.product'].browse(int(line.product_id.id))
                MembershipPackage = self.env['membership.package'].search([
                    ('product_id', '=', int(ProductProduct.product_tmpl_id))
                ], limit=1)
                if MembershipPackage.id:
                    partner_id = line.invoice_id.partner_id.id
                    MembershipMember = self.env['membership.member'].search([
                        ('partner_id', '=', int(partner_id))
                    ], limit=1)
                    if MembershipMember.id:
                        self.env['membership.member'].browse(int(MembershipMember.id)).unlink

                    self.env['membership.member'].create({
                        'package_id': MembershipPackage.product_id,
                        'partner_id': partner_id,
                        'discount': MembershipPackage.discount,
                        'membership_start': datetime.now().strftime("%Y-%m-%d"),
                        'membership_stop': (datetime.now() + timedelta(days=int(MembershipPackage.duration))).strftime("%Y-%m-%d"),

                    })
        return res

    @api.model
    def create(self, vals):
        invoice_line = super(AccountInvoiceLine, self).create(vals)
        if invoice_line.invoice_id.type == 'out_invoice' and \
                invoice_line.product_id.type == 'membership' :
            ProductProduct = self.env['product.product'].browse(int(invoice_line.product_id.id))
            MembershipPackage = self.env['membership.package'].search([
                ('product_id', '=', int(ProductProduct.product_tmpl_id))
            ], limit=1)
            if MembershipPackage.id:
                partner_id = invoice_line.invoice_id.partner_id.id
                MembershipMember = self.env['membership.member'].search([
                    ('partner_id', '=', int(partner_id))
                ], limit=1)
                if MembershipMember.id:
                    self.env['membership.member'].browse(int(MembershipMember.id)).unlink

                self.env['membership.member'].create({
                    'package_id': MembershipPackage.product_id,
                    'partner_id': partner_id,
                    'discount': MembershipPackage.discount,
                    'membership_start': datetime.now().strftime("%Y-%m-%d"),
                    'membership_stop': (datetime.now() + timedelta(days=int(MembershipPackage.duration))).strftime("%Y-%m-%d"),

                })
        return invoice_line
