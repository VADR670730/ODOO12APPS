# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp



class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    discount_global = fields.Float(string='Global Discount', digits=dp.get_precision('Discount'), default=0.0)


    @api.onchange('discount_global')
    def global_discount(self):
        if self.discount_global:
            for rec in self.order_line:
                rec.discount += self.discount_global


