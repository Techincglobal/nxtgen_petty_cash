# Copyright (c) 2025, techincglobal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PettyCashBox(Document):
	@property
	def balance_amount(self):
		sql=f"""SELECT 
			sum(`tabPetty cash Ledger`.received_dr)- sum(`tabPetty cash Ledger`.paid_cr) as 'ball'	
			FROM
			`tabPetty cash Ledger`
			WHERE
			`tabPetty cash Ledger`.is_cancel <> 1 AND
			`tabPetty cash Ledger`.petty_cash_box = '{self.name}';"""
		res=frappe.db.sql(sql, as_dict=1)
		if res and res[0].ball:
			return res[0].ball
		else:
			return 0
	@property
	def outstanding_amount(self):
		sql=f"""SELECT
			sum(`tabIOU  Request`.disbursed_ammount) as 'oustanding'
			FROM	
			`tabIOU  Request`
			WHERE
			`tabIOU  Request`.petty_cash_box = '{self.name}' AND
			`tabIOU  Request`.docstatus = 1 AND
			`tabIOU  Request`.`status` <> 'Settled';"""
		res=frappe.db.sql(sql, as_dict=1)
		if res and res[0].oustanding:
			return res[0].oustanding
		else:
			return 0
