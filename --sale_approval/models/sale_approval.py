from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError


class SaleApprovalSettings(models.Model):
    _name = 'sale.approval.settings'
    _description ='Sale Approval Settings'
    _rec_name = 'code'


    code = fields.Char(string="Code",readonly=True, required=True, copy=False, default='New')
    approval_currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    minimum_total_amount = fields.Float(string='Minimum Total Amount', required=True,default=1.00)
    maximum_total_amount = fields.Float(string='Maximum Total Amount', required=True)
    level_one_id = fields.Many2one('res.users',string= "Approval User", required=True)


    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('sale.approval.settings') or 'New'
        result = super(SaleApprovalSettings, self).create(vals)
        return result


    @api.constrains('maximum_total_amount','minimum_total_amount')
    def maximum(self):
        if self.minimum_total_amount >= self.maximum_total_amount:
            raise UserError(_("You Have To Enter The Maximum Total Amount above The Minimum Total Amount"))
        if self.minimum_total_amount < 1.00:
            raise UserError(_("You have to enter at least 1 Rs For Minimum Total Amount"))



    @api.constrains('minimum_total_amount')
    def minimum(self):
        min = self.env['sale.approval.settings'].search([('approval_currency_id', '=', self.approval_currency_id.id),
                                                         ('id', '!=', self.id)])
        for rec in min:
            value = rec.maximum_total_amount
            if self.minimum_total_amount <= rec.maximum_total_amount:
                raise UserError(_("Please check The Minimum value"))



