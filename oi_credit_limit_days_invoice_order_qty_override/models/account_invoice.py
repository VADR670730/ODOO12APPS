from odoo import api, fields, models, _
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class Invoice(models.Model):
    _inherit = 'account.invoice'

    override_credit_limit = fields.Boolean("Override Credit Limit")
    today_date = fields.Date(string="Current Date", default=fields.Date.today)

    @api.multi
    def action_invoice_open(self):
        if self.type == 'out_invoice':
            if self.partner_id.credit_limit:
                invoice_total = 0
                payment_total = 0
                exceed_amount = 0
                due = 0

                customer_invoices = self.env["account.invoice"].search([('partner_id','=', self.partner_id.id), ('state','not in',['draft','cancel','paid']),('type', '=','out_invoice')])
                customer_inv = self.env["account.invoice"].search([('partner_id','=', self.partner_id.id), ('state','not in',['draft','cancel']),('type', '=','out_invoice')])
                for inv in customer_inv:
                    invoice_total+= inv.amount_total
                    due += inv.residual
                    print ("dueeee",invoice_total,due)
                # customer_payment = self.env["account.payment"].search([('partner_id','=', self.partner_id.id), ('payment_type', '=','inbound'),('state','in',['posted','reconciled'])])
                # for pay in customer_payment:
                    payment_total = invoice_total - due
                    print ('payment_total',payment_total)
                sale = self.env['sale.order'].search([('name','=',self.origin)])
                ordered_quantity = all(line.product_id.invoice_policy == 'order' for line in self.invoice_line_ids)
                cus_amount = self.amount_total
                print ("Customer Amount",cus_amount)
                if self.partner_id.credit_limit and not self.override_credit_limit and self.partner_id.credit_limit_applicable:
                    if cus_amount >= self.partner_id.credit_limit:
                        raise UserError(_('Credit limit exceeded for this customer'))
                for rec in customer_invoices:
                    if self.partner_id.date_credit_limit:
                        print("Total Invoice",rec)
                        today = self.today_date
                        print("Today ",today)
                        invoice = rec.date_invoice
                        print("Invoice ",invoice)
                        dates_cou = self.partner_id.date_credit_limit
                        print("Dates_cou ",dates_cou)
                        deltaas = today - invoice
                        print("Total Days",deltaas.days)
                        invoice_expiry = (deltaas).days
                        print("Expiry",invoice_expiry)

                        if invoice_expiry > self.partner_id.date_credit_limit:
                            print ("UserError")
                            raise UserError(_('Days limit exceeded for this customer'))

                print ("Invoice ",customer_invoices)
                for record in customer_invoices:
                    invoice_count = len(customer_invoices)
                    invoice_count_total = self.partner_id.invoice_credit_limit
                    print ("Invoice Count",invoice_count)
                    if invoice_count_total:
                        print ("Total Invoice", invoice_count)
                        print ("Total Invoice Limit",invoice_count)
                        if invoice_count >= invoice_count_total:
                            print ("UserError")
                            raise UserError(_('Invoice limit exceeded for this customer'))
                if payment_total > invoice_total:
                    print ("else")
                    to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
                    if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                        raise UserError(_("Invoice must be in draft state in order to validate it."))
                    if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
                        raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
                    to_open_invoices.action_date_assign()
                    to_open_invoices.action_move_create()
                    return to_open_invoices.invoice_validate()
                if invoice_total > payment_total:
                    exceed_amount = (invoice_total + self.amount_total) - payment_total
                    print ("exc",exceed_amount)
                if ordered_quantity:
                    if self.partner_id.credit_limit and self.partner_id.credit_limit_applicable:

                        if exceed_amount > self.partner_id.credit_limit:
                            print (self.override_credit_limit, "self.override_credit_limit")
                            if self.override_credit_limit:
                                to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
                                if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                                    raise UserError(_("Invoice must be in draft state in order to validate it."))
                                if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
                                    raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
                                to_open_invoices.action_date_assign()
                                to_open_invoices.action_move_create()
                                return to_open_invoices.invoice_validate()
                            else:
                                raise UserError(_('Credit limit exceeded for this customer'))
                        else:
                            to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
                            if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                                raise UserError(_("Invoice must be in draft state in order to validate it."))
                            if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
                                raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
                            to_open_invoices.action_date_assign()
                            to_open_invoices.action_move_create()
                            return to_open_invoices.invoice_validate()
                else:
                    raise UserError(_('Select all products with Ordered quantities Invoicing policy'))
            else:
                to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
                if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
                    raise UserError(_("Invoice must be in draft state in order to validate it."))
                if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
                    raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
                to_open_invoices.action_date_assign()
                to_open_invoices.action_move_create()
                return to_open_invoices.invoice_validate()