from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError,Warning



class PurchaseOrderInherits(models.Model):
    _inherit = "purchase.order"


    level_one_id = fields.Many2one('res.users', compute='amount_total_onchange', string="Level 1",readonly=True)
    level_two_id = fields.Many2one('res.users', compute='amount_total_onchange',string="Level 2",readonly=True)

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('to approve two', 'To Approve two'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)


    def button_approves(self, force=False):

        if self.level_one_id and not self.level_two_id:
            if self.env.user.name == self.level_one_id.name:
                self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
            else:
                raise UserError('You’re not allocated as Level-1 approver for this PO.')


        if self.level_one_id and self.level_two_id:
            if self.env.user.name == self.level_one_id.name:
                self.write({'state': 'to approve two', 'date_approve': fields.Date.context_today(self)})
            else:
                raise UserError('You’re not allocated as Level-1 approver for this PO.')

        return {}


    def button_approve(self, force=False):
        if self.level_two_id and not self.level_one_id:
            if self.env.user.name == self.level_two_id.name:
                self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
            else:
                raise UserError('You’re not allocated as Level-2 approver for this PO.')


        if self.level_one_id and self.level_two_id:
            if self.env.user.name == self.level_two_id.name:
                self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
                self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
            else:
                raise UserError('You’re not allocated as Level-2 approver for this PO.')
        return {}

    @api.onchange('amount_total')
    def amount_total_onchange(self):
        if self.amount_total:
            max = self.env['purchase.approval.settings'].search([('minimum_total_amount', '<=', self.amount_total),
                                                                 ('maximum_total_amount', '>=', self.amount_total),
                                                                 ('approval_currency_id.name', '=', self.currency_id.name)])
            self.level_one_id = max.level_one_id
            self.level_two_id = max.level_two_id

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()

            if order.user_has_groups('purchase_approval.group_no_approval_restrictions'):
                self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
                self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})

            if not order.user_has_groups('purchase_approval.group_no_approval_restrictions'):
                max = self.env['purchase.approval.settings'].search([('minimum_total_amount', '<=',order.amount_total),
                                                                     ('maximum_total_amount', '>=',order.amount_total),
                                                                     ('approval_currency_id.name', '=', order.currency_id.name)])

                if not max.level_two_id and not max.level_one_id:
                    raise UserError('Approval Limit is not fixed: Kindly check Levels,Value & Currency.')

                if max.maximum_total_amount < order.amount_total:
                    raise UserError('Approval Limit is not fixed: Kindly check Levels,Value & Currency.')

                if max.level_two_id and not max.level_one_id:
                    order.write({'state': 'to approve two'})

                if max.level_one_id:
                    if max.minimum_total_amount <= order.amount_total and max.maximum_total_amount >= order.amount_total:
                        order.write({'state': 'to approve'})

        return True


