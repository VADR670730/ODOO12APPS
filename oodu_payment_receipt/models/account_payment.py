# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp



class AccountPayment(models.Model):
    _inherit = "account.payment"

    reference = fields.Char("Memo")

