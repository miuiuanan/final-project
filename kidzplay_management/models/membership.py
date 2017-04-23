# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    # membership_type = fields.Selection(membership.TYPE, compute='_compute_membership_type',
    #     string='Current Membership Type', store=True)
    # @api.model
    # def _get_membership_product(self):
    #     res = []
    #
    #     products = self.env['product.template']
    #     for product in products:
    #         if (product.membership == True):
    #             res.append((product.id, product.name))
    #     return res
    # @api.model
    # def _get_membership_product(self):
    #     products = self.env['product.template']
    #     for product in products:
    #         if (product.id == 1):
    #             product.list_price = 123
    #             product.update(product)
    # membership_type = fields.Selection(selection=_get_membership_product, string='Membership Type')
    # membership_type = fields.Selection(selection=[('1', '1'), ('2','2')], string='Membership Type')
    # membership_type = '1';




    # def _get_mailing_model(self):
    #     res = []
    #     for model_name in self.env:
    #         model = self.env[model_name]
    #         if hasattr(model, '_mail_mass_mailing') and getattr(model, '_mail_mass_mailing'):
    #             if getattr(model, 'message_mass_mailing_enabled'):
    #                 res.append((model._name, model.message_mass_mailing_enabled()))
    #             else:
    #                 res.append((model._name, model._mail_mass_mailing))
    #     res.append(('mail.mass_mailing.contact', _('Mailing List')))
    #     return res