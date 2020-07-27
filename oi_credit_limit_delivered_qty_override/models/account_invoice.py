from odoo import api, fields, models, _
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils

class Invoice(models.Model):
    _inherit = 'account.invoice'

  
    today_date = fields.Date(string="Current Date", default=fields.Date.today)

    @api.multi
    def action_invoice_open(self):
        cus_inv = self.env["account.invoice"].search([('partner_id','=', self.partner_id.id),('state','in',['open']),('type', '=','out_invoice')])
        cus_amount = self.amount_total
        print ("Customer Amount",cus_amount)
        if self.partner_id.credit_limit > 0 and self.partner_id.credit_limit_applicable ==True:
            if cus_amount > self.partner_id.credit_limit:
                raise UserError(_('Credit limit exceeded for this customer'))
        
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: not inv.partner_id):
            raise UserError(_("The field Vendor is required, please complete it to validate the Vendor Bill."))
        if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
            raise UserError(_("Invoice must be in draft state in order to validate it."))
        if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        if to_open_invoices.filtered(lambda inv: not inv.account_id):
            raise UserError(_('No account was found to create the invoice, be sure you have installed a chart of account.'))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        return to_open_invoices.invoice_validate()
         