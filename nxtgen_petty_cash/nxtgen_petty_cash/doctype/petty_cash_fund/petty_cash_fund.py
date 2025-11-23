import frappe
from frappe.model.document import Document
from frappe.utils import cint, comma_or, flt, getdate, nowdate

class PettyCashFund(Document):
	def on_submit(self):
		petty_cash_ledger = frappe.get_doc({
			'doctype': 'Petty cash Ledger',
			'date': getdate(),
			'petty_cash_box': self.petty_cash_box,
			'voucher_type':self.doctype,
			'voucher_no': self.name,
   			'transaction_type':"Receipt",
			'received_dr':self.request_amount
		})
		petty_cash_ledger.insert(ignore_permissions=True)
@frappe.whitelist()
def make_payment_entry(dt, dn):
	doc = frappe.get_doc(dt, dn)
	pe = frappe.new_doc("Payment Entry")
	# pe.payment_type = "Pay"
	pe.payment_type = "Internal Transfer"
	pe.posting_date = nowdate()
	# pe.party_type = "Petty Cash Box"
	# pe.party = doc.petty_cash_box
	pe.paid_to_account_currency="LKR"
	# pe.company = doc.company
	pe.mode_of_payment = "Cash"
	pe.paid_from = ""
	pe.paid_to = doc.account
	pe.paid_amount = doc.request_amount	
	pe.received_amount = doc.request_amount
	# pe.append(
	# 				"references",
	# 				{
	# 					"reference_doctype":"Petty Cash Box",
	# 					"reference_name": doc.petty_cash_box,
	# 					# "bill_no": doc.get("bill_no"),
	# 					"due_date": doc.get("required_on"),
	# 					"total_amount": doc.request_amount,
	# 					"outstanding_amount": doc.request_amount,
	# 					"allocated_amount": doc.request_amount,
	# 				},
	# 			)
	return pe
	# return erpnext.accounts.utils.make_payment_entry(
	# 	"Petty Cash Fund",
	# 	doc.name
	# )