# -*- coding:utf-8 -*-
from odoo import fields, models, api
import time

class MembershipPartner(models.Model):
	_inherit = "res.partner"

	membership_status_rel = fields.Char(compute="_compute_membership", store=True)
	membership_type_rel = fields.Char(compute="_compute_membership", store=False)
	membership_start_rel = fields.Char(compute="_compute_membership", store=False)
	membership_end_rel = fields.Char(compute="_compute_membership", store=False)
	membership_discount_rel = fields.Char(compute="_compute_membership", store=False)
    membership_dob = fields.Date(string="Children birthday", store=True)

	@api.multi
	def _compute_membership(self):
		for record in self:
			if record.id > 1:
				membership_id = self.env['membership.member'].search([(
					'partner_id', '=', record.id
					)], limit=1)
				if membership_id:
					# Membership status
					record.membership_status_rel = membership_id.membership_status
					self.env['res.partner'].browse(int(record.id)).write({
						'membership_status_rel': record.membership_status_rel,
						})
					print record.membership_status_rel
					# Membership start-end
					record.membership_start_rel = membership_id.membership_start
					record.membership_end_rel = membership_id.membership_stop

					# Membership package details
					tmp_type = membership_id.package_id
					print tmp_type
					membership_id = self.env['membership.package'].search([(
						'product_id', '=', tmp_type
						)], limit=1)
					record.membership_type_rel = membership_id.name
					record.membership_discount_rel = str(membership_id.discount) + " %"
					print record.membership_discount_rel
					print record.membership_type_rel
