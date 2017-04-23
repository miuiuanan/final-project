# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from . import membership
import time
from datetime import datetime
from datetime import timedelta


class Partner(models.Model):
    _inherit = 'res.partner'

    associate_member = fields.Many2one('res.partner', string='Associate Member',
        help="A member with whom you want to associate your membership. "
             "It will consider the membership state of the associated member.")
    member_lines = fields.One2many('membership.membership_line', 'partner', string='Membership')
    free_member = fields.Boolean(string='Free Member',
        help="Select if you want to give free membership.")
    membership_amount = fields.Float(string='Membership Amount', digits=(16, 2),
        help='The price negotiated by the partner')
    membership_state = fields.Selection(membership.STATE, compute='_compute_membership_state',
        string='Current Membership Status', store=True,
        help='It indicates the membership state.\n'
             '-Non Member: A partner who has not applied for any membership.\n'
             '-Cancelled Member: A member who has cancelled his membership.\n'
             '-Old Member: A member whose membership date has expired.\n'
             '-Waiting Member: A member who has applied for the membership and whose invoice is going to be created.\n'
             '-Invoiced Member: A member whose invoice has been created.\n'
             '-Paying member: A member who has paid the membership fee.')
    membership_start = fields.Date(compute='_compute_membership_start',
        string ='Membership Start Date', store=True,
        help="Date from which membership becomes active.")
    membership_stop = fields.Date(compute='_compute_membership_stop',
        string ='Membership End Date', store=True,
        help="Date until which membership remains active.")
    membership_duration = fields.Date(compute='_compute_membership_duration')
    membership_cancel = fields.Date(compute='_compute_membership_cancel',
        string ='Cancel Membership Date', store=True,
        help="Date on which membership has been cancelled")

    membership_type = fields.Integer(string='Membership Type')
    membership_state_type = fields.Char(string='Membership Type', compute='_compute_membership_type', store=True)
    membership_discount = fields.Float(string='Membership Discount', compute='_compute_membership_type', store=True)

    @api.depends('member_lines.account_invoice_line.invoice_id.state',
                 'member_lines.account_invoice_line.invoice_id.invoice_line_ids',
                 'member_lines.account_invoice_line.invoice_id.payment_ids',
                 'free_member',
                 'member_lines.date_to', 'member_lines.date_from',
                 'associate_member.membership_state')
    def _compute_membership_state(self):
        values = self._membership_state()
        for partner in self:
            partner.membership_state = values[partner.id]
    @api.depends('membership_type')
    def _compute_membership_type(self):
        for partner in self:
            partner.membership_discount = 0
            product_membership = self.env['product.template'].search([
                ('id', '=', partner.membership_type)
            ], limit=1)
            if (product_membership.name):
                partner.membership_state_type = product_membership.name
            if (product_membership.membership_discount):
                partner.membership_discount = product_membership.membership_discount
    @api.depends('member_lines.account_invoice_line.invoice_id.state',
                 'member_lines.account_invoice_line.invoice_id.invoice_line_ids',
                 'member_lines.account_invoice_line.invoice_id.payment_ids',
                 'free_member',
                 'member_lines.date_to', 'member_lines.date_from',
                 'associate_member.membership_state',
                 'membership_type')
    def _compute_membership_duration(self):
        for partner in self:
            product_membership = self.env['product.template'].search([
                ('id', '=', partner.membership_type)
            ], limit=1)
            # partner.membership_duration = self.env['product.template'].search([
            #     ('partner', '=', partner.associate_member.id or partner.id), ('date_cancel', '=', False)
            # ], limit=1, order='date_duration').date_duration
            partner.membership_duration = product_membership.date_duration

    @api.depends('member_lines.account_invoice_line.invoice_id.state',
                 'member_lines.account_invoice_line.invoice_id.invoice_line_ids',
                 'member_lines.account_invoice_line.invoice_id.payment_ids',
                 'free_member',
                 'member_lines.date_to', 'member_lines.date_from',
                 'membership_state',
                 'associate_member.membership_state','membership_type')
    def _compute_membership_start(self):
        """Return  date of membership"""

        for partner in self:
            partner.membership_start = datetime.now().strftime("%Y-%m-%d")
            # partner.membership_start = self.env['membership.membership_line'].search([
            #     ('partner', '=', partner.associate_member.id or partner.id), ('date_cancel','=',False)
            # ], limit=1, order='date_duration desc').date_duration

    @api.depends('member_lines.account_invoice_line.invoice_id.state',
                 'member_lines.account_invoice_line.invoice_id.invoice_line_ids',
                 'member_lines.account_invoice_line.invoice_id.payment_ids',
                 'free_member',
                 'member_lines.date_to', 'member_lines.date_from',
                 'membership_state',
                 'associate_member.membership_state','membership_type')
    def _compute_membership_stop(self):
        for partner in self:
            # duration = self.env['membership.membership_line'].search([
            #     ('partner', '=', partner.associate_member.id or partner.id),('date_cancel','=',False)
            # ], limit=1, order='date_to desc').date_duration
            duration = self.env['product.template'].search([
                ('id', '=', partner.membership_type)
            ], limit=1).membership_duration
            if duration:
                partner.membership_stop = (datetime.now() + timedelta(days=int(duration))).strftime("%Y-%m-%d")


    @api.depends('member_lines.account_invoice_line.invoice_id.state',
                 'member_lines.account_invoice_line.invoice_id.invoice_line_ids',
                 'member_lines.account_invoice_line.invoice_id.payment_ids',
                 'free_member',
                 'member_lines.date_to', 'member_lines.date_from',
                 'membership_state',
                 'associate_member.membership_state')
    def _compute_membership_cancel(self):
        for partner in self:
            if partner.membership_state == 'canceled':
                partner.membership_cancel = self.env['membership.membership_line'].search([
                    ('partner', '=', partner.id)
                ], limit=1, order='date_cancel').date_cancel
            else:
                partner.membership_cancel = False

    def _membership_state(self):
        """This Function return Membership State For Given Partner. """
        res = {}
        today = fields.Date.today()
        for partner in self:
            res[partner.id] = 'none'

            if partner.membership_cancel and today > partner.membership_cancel:
                res[partner.id] = 'free' if partner.free_member else 'canceled'
                continue
            # if partner.membership_stop and today > partner.membership_stop:
            #     res[partner.id] = 'free' if partner.free_member else 'old'
            #     continue

            s = 4
            if partner.member_lines:
                for mline in partner.member_lines:
                    if mline.date_to >= today and mline.date_from <= today:
                        if mline.account_invoice_line.invoice_id:
                            mstate = mline.account_invoice_line.invoice_id.state
                            if mstate == 'paid':
                                s = 0
                                inv = mline.account_invoice_line.invoice_id
                                for payment in inv.payment_ids:
                                    if any(payment.invoice_ids.filtered(lambda inv: inv.type == 'out_refund')):
                                        s = 2
                                break
                            elif mstate == 'open' and s != 0:
                                s = 1
                            elif mstate == 'cancel' and s != 0 and s != 1:
                                s = 2
                            elif  (mstate == 'draft' or mstate == 'proforma') and s != 0 and s != 1:
                                s = 3
                if s == 4:
                    for mline in partner.member_lines:
                        if mline.date_from < today and mline.date_to < today and mline.date_from <= mline.date_to and mline.account_invoice_line and mline.account_invoice_line.invoice_id.state == 'paid':
                            s = 5
                        else:
                            s = 6
                if s == 0:
                    res[partner.id] = 'paid'
                elif s == 1:
                    res[partner.id] = 'invoiced'
                elif s == 2:
                    res[partner.id] = 'canceled'
                elif s == 3:
                    res[partner.id] = 'waiting'
                elif s == 5:
                    res[partner.id] = 'old'
                elif s == 6:
                    res[partner.id] = 'none'
            if partner.free_member and s != 0:
                res[partner.id] = 'free'
            if partner.associate_member:
                res_state = partner.associate_member._membership_state()
                res[partner.id] = res_state[partner.associate_member.id]
        return res

    @api.one
    @api.constrains('associate_member')
    def _check_recursion(self):
        level = 100
        while self:
            self = self.associate_member
            if not level:
                raise ValidationError(_('Error ! You cannot create recursive associated members.'))
            level -= 1

    @api.model
    def _cron_update_membership(self):
        # used to recompute 'membership_state'; should no longer be necessary
        pass

    @api.multi
    def create_membership_invoice(self, product_id=None, datas=None):
        """ Create Customer Invoice of Membership for partners.
        @param datas: datas has dictionary value which consist Id of Membership product and Cost Amount of Membership.
                      datas = {'membership_product_id': None, 'amount': None}
        """
        product_id = product_id or datas.get('membership_product_id')
        amount = datas.get('amount', 0.0)
        invoice_list = []
        for partner in self:
            addr = partner.address_get(['invoice'])
            if partner.free_member:
                raise UserError(_("Partner is a free Member."))
            if not addr.get('invoice', False):
                raise UserError(_("Partner doesn't have an address to make the invoice."))
            invoice = self.env['account.invoice'].create({
                'partner_id': partner.id,
                'account_id': partner.property_account_receivable_id.id,
                'fiscal_position_id': partner.property_account_position_id.id
            })
            line_values = {
                'product_id': product_id,
                'price_unit': amount,
                'invoice_id': invoice.id,
            }
            # create a record in cache, apply onchange then revert back to a dictionnary
            invoice_line = self.env['account.invoice.line'].new(line_values)
            invoice_line._onchange_product_id()
            line_values = invoice_line._convert_to_write({name: invoice_line[name] for name in invoice_line._cache})
            line_values['price_unit'] = amount
            invoice.write({'invoice_line_ids': [(0, 0, line_values)]})
            invoice_list.append(invoice.id)
            invoice.compute_taxes()
        return invoice_list

    @api.depends('account_invoice_line.invoice_id.state',
                 'account_invoice_line.invoice_id.payment_ids',
                 'account_invoice_line.invoice_id.payment_ids.invoice_ids.type')
    def _compute_state(self):
        """Compute the state lines """
        Invoice = self.env['account.invoice']
        for line in self:
            self._cr.execute('''
                SELECT i.state, i.id FROM
                account_invoice i
                WHERE
                i.id = (
                    SELECT l.invoice_id FROM
                    account_invoice_line l WHERE
                    l.id = (
                        SELECT  ml.account_invoice_line FROM
                        membership_membership_line ml WHERE
                        ml.id = %s
                        )
                    )
                ''', (line.id,))
            fetched = self._cr.fetchone()
            if not fetched:
                line.state = 'canceled'
                continue
            istate = fetched[0]
            if istate in ('draft', 'proforma'):
                line.state = 'waiting'
            elif istate == 'open':
                line.state = 'invoiced'
            elif istate == 'paid':
                line.state = 'paid'
                invoices = Invoice.browse(fetched[1]).payment_ids.mapped('invoice_ids')
                if invoices.filtered(lambda invoice: invoice.type == 'out_refund'):
                    line.state = 'canceled'
            elif istate == 'cancel':
                line.state = 'canceled'
            else:
                line.state = 'none'

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # @api.multi
    # def write(self, vals):
    #     PartnerLine = self.env['res.partner']
    #     res = super(AccountInvoiceLine, self).write(vals)
    #     for line in self.filtered(lambda line: line.invoice_id.type == 'out_invoice'):
    #         partner_lines = PartnerLine.search([('id', '=', line.partner_id)])
    #         if line.product_id.membership and not partner_lines:
    #             # Product line has changed to a membership product
    #             # date_from = line.product_id.membership_date_from
    #             # date_to = line.product_id.membership_date_to
    #             membership_start = datetime.now().strftime("%Y-%m-%d")
    #             membership_stop = (datetime.now() + timedelta(days=int(line.product_id.duration))).strftime("%Y-%m-%d")
    #
    #             PartnerLine.write({
    #                 'membership_start': membership_start,
    #                 'membership_stop': membership_stop,
    #                 'membership_discount': line.product_id.membership_discount,
    #                 'membership_type': line.product_id.id,
    #                 'membership_state_type': line.product_id.name,
    #             })
    #         if line.product_id and not line.product_id.membership and partner_lines:
    #             # Product line has changed to a non membership product
    #             partner_lines.unlink()
    #     return res

    @api.model
    def create(self, vals):
        PartnerLine = self.env['res.partner']
        invoice_line = super(AccountInvoiceLine, self).create(vals)
        if invoice_line.invoice_id.type == 'out_invoice' and \
                invoice_line.product_id.membership :
            # Product line is a membership product
            # date_from = invoice_line.product_id.membership_date_from
            # date_to = invoice_line.product_id.membership_date_to

            # membership_start = datetime.now().strftime("%Y-%m-%d")
            # membership_stop = (datetime.now() + timedelta(days=int(invoice_line.product_id.duration))).strftime("%Y-%m-%d")
            product_id = self.env['product.product'].search([
                ('id', '=', invoice_line.product_id.id)
            ], limit=1).product_tmpl_id
            productTemplate = self.env['product.template'].search([
                ('id', '=', int(product_id))
            ], limit=1)
            self.env['res.partner'].browse(int(invoice_line.partner_id)).write({
                'membership_type': product_id,
            })
            # PartnerLine.write({
            #     # 'membership_start': membership_start,
            #     # 'membership_stop': membership_stop,
            #     # 'membership_discount': productTemplate.membership_discount,
            #     'membership_type': product_id,
            #     # 'membership_state_type': productTemplate.name,
            # })
        return invoice_line
