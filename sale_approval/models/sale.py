from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError,Warning

class SaleOrderInherits(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('to approve', 'To Approve'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    level_one_id = fields.Many2one('res.users', compute='sale_amount_total', string="Approval User", readonly=True)

    @api.onchange('amount_total')
    def sale_amount_total(self):
        if self.amount_total:
            sale = self.env['sale.approval.settings'].search([('minimum_total_amount', '<=', self.amount_total),
                                                                 ('maximum_total_amount', '>=', self.amount_total),
                                                                 ('approval_currency_id.name', '=', self.currency_id.name)])
            if self.user_has_groups('sale_approval.group_so_no_approval_restrictions'):
                self.level_one_id = False
            else:
                self.level_one_id = sale.level_one_id


    def to_approval(self):
        if self.level_one_id:
            if self.env.user.name == self.level_one_id.name:
                self.write({'state': 'sale', 'date_order': fields.Datetime.now()})
                self._action_confirm()
            else:
                raise UserError('You’re not allocated as Approval User for this SO.')
        return {}


    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])

        if self.user_has_groups('sale_approval.group_so_no_approval_restrictions'):
            self.write({
                'state': 'sale',
                'date_order': fields.Datetime.now()
            })
            self._action_confirm()


        if not self.user_has_groups('sale_approval.group_so_no_approval_restrictions'):
            sale = self.env['sale.approval.settings'].search([('minimum_total_amount', '<=', self.amount_total),
                                                                 ('maximum_total_amount', '>=', self.amount_total),
                                                                 ('approval_currency_id.name', '=',self.currency_id.name)])

            if not sale.level_one_id:
                raise UserError('Approval Limit is not fixed: Kindly check Aprroval User,Value & Currency.')

            if sale.maximum_total_amount < self.amount_total:
                raise UserError('Approval Limit is not fixed: Kindly check Aprroval User,Value & Currency.')


            if sale.level_one_id:
                if sale.minimum_total_amount <= self.amount_total and sale.maximum_total_amount >= self.amount_total:
                    self.write({'state': 'to approve'})


        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True