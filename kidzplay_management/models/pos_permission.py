# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PermissionRel(models.Model):
    _name = 'pos.permission.rel'

class Users(models.Model):
    _name = 'pos.permission'

    permission_id = fields.Many2one('pos.permission.rel', string='User', required=True, index=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Object', required=True, index=True, ondelete='cascade')
    perm_discount = fields.Boolean(string='Can discount')
    perm_price = fields.Boolean(string='Can change price')

class PermissionInherit(models.Model):
    _inherit = 'pos.permission.rel'

    permission_access = fields.One2many('pos.permission', 'permission_id', string='Access Controls')
    name = fields.Char(string='Name', default="Permission")

    @api.multi
    def unlink(self):
        res = super(PermissionRel, self).unlink()
        self.create(
            { 'name': 'Permission'}
        )
        return res

