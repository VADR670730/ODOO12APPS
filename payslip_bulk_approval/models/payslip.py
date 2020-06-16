from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPayslipInherit(models.Model):
	_inherit = 'hr.payslip'

	@api.multi
	def action_approve(self):
		for each in self:
			if each.state == 'verify':
				each.write({'state': 'done'})
			else:
				raise UserError(_("You can't select the Draft records."))
		return True
