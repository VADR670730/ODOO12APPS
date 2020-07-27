from odoo import api, fields, models, _
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class Invoice(models.Model):
    _inherit = 'account.invoice'


    @api.multi
    def action_invoice_open(self):
        
        invoice_total = 0
        payment_total = 0
        exceed_amount = 0
        due = 0

        customer_inv = self.env["account.invoice"].search([('partner_id','=', self.partner_id.id), ('state','not in',['draft','cancel']),('type', '=','out_invoice')])
        for inv in customer_inv:
            invoice_total+= inv.amount_total
            due += inv.residual
            payment_total = invoice_total - due
            print ('payment_total',payment_total)
        
        sale = self.env['sale.order'].search([('name','=',self.origin)])

        if payment_total > invoice_total:
            print ("else")
            res = super(Invoice, self).action_invoice_open()
            return res
        if invoice_total > payment_total:
            exceed_amount = (invoice_total + sale.amount_total) - payment_total

        if exceed_amount > self.partner_id.credit_limit:
            raise UserError(_('Credit limit exceeded for this customer'))
        else:
            res = super(Invoice, self).action_invoice_open()
            return res

