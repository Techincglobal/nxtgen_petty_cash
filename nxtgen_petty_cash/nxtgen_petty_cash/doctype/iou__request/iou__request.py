# Copyright (c) 2025, techincglobal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IOURequest(Document):
	# pass
	def on_insert(self):
		self.status="Pending"
		self.send_notification()
  
	def send_notification(self):
		pass

@frappe.whitelist()
def get_expences_approval(employee):
	approval = frappe.db.get_value("Employee", employee, "expense_approver")
	return approval

