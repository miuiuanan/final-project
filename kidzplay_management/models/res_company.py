# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    wifi = fields.Char(string='Wifi')
    wifi_pass = fields.Char(string='Wifi password')

