from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPayslipInherit(models.Model):
	_inherit = 'hr.payslip'


	@api.multi
	def action_approve(self):
		self.write({'state': 'done'})
		return True
