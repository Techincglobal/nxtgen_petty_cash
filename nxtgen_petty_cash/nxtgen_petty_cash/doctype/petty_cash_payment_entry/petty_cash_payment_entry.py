# Copyright (c) 2025, techincglobal and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from frappe.model.document import Document
from erpnext.accounts.general_ledger import make_gl_entries
from frappe.model.delete_doc import delete_doc
from frappe.utils import cstr, flt, get_link_to_form


class PettyCashPaymentEntry(Document):
	# pass\
	def on_submit(self):
		self.make_gl_entries()
	def on_cancel(self):
		self.ignore_linked_doctypes = ("GL Entry", "Payment Ledger Entry")
		self.make_gl_entries(cancel=True)
		# self.delete_gl_entries()
	
	def make_gl_entries(self, cancel=False):
		self.is_opening_entry = 0
		if self.cost_center:
			default_cost_center = self.cost_center
		else:
			default_cost_center = frappe.db.get_value("Company", self.company, "cost_center")
		# gl_entries = []
		for item in self.items:
			gl_entries = []
			# debit entry
			acc = frappe.db.get_value("IOU  Request", item.iou_request, ['petty_cash_box'], as_dict=1)
			PettyCashAccount = frappe.db.get_value("Petty Cash Box", acc.petty_cash_box, "account")
			expencesAccount = get_expense_claim_account(item.claim_type, self.company)
			# remarks = f"IOU disbursed to {self.loan_applicant}"
			gl_entries.append(self.get_gl_dict({
				"account": expencesAccount.get('account'),#Expenses Account
				"against": PettyCashAccount,#Petty Cash Account
				"debit": item.amount,
				"debit_in_account_currency": item.amount,
				"remarks": f"Petty Cash Payment for {item.description}",
				# "party_type": "IOU Settlement",
				# "party": item.iou_settlement,
				"cost_center": default_cost_center,
				"is_opening" : self.is_opening_entry,
			}))

			# credit entry
			gl_entries.append(self.get_gl_dict({
				"account": PettyCashAccount,#Petty Cash Account
				"against": expencesAccount.get('account'),#Expenses Account
				"credit": item.amount,
				"credit_in_account_currency": item.amount,
				"remarks": f"Petty Cash Payment for {item.description}",
				# "party_type": "IOU Settlement",
				# "party": item.iou_settlement,
				"cost_center": default_cost_center,
				"is_opening" : self.is_opening_entry,
			}))
	
			# frappe.msage(_("GL Entries for {0}").format(cstr(gl_entries)))	
			make_gl_entries(gl_entries, cancel=cancel, update_outstanding="No")
			frappe.db.set_value("IOU Settlement", item.iou_settlement, "is_gl_done", 1)
		# remarks = f"IOU disbursed to {self.loan_applicant}"

		# # debit entry
		# gl_entries.append(self.get_gl_dict({
		# 	"account": self.loan_account,
		# 	"against": self.disbursement_account,
		# 	"debit": self.loan_amount,
		# 	"debit_in_account_currency": self.loan_amount,
		# 	"remarks": remarks,
		# 	"party_type": "Employee",
		# 	"party": self.loan_applicant,
		# 	"is_opening" : self.is_opening_entry,
		# }))

		# # credit entry
		# gl_entries.append(self.get_gl_dict({
		# 	"account": self.disbursement_account,
		# 	"against": self.loan_account,
		# 	"credit": self.loan_amount,
		# 	"credit_in_account_currency": self.loan_amount,
		# 	"remarks": remarks,
		# 	"is_opening" : self.is_opening_entry,
		# }))

		# make_gl_entries(gl_entries, cancel=cancel, update_outstanding="No")


	def get_gl_dict(self, args):
		"""Return a GL entry dict with default values populated"""
		from erpnext.accounts.utils import get_fiscal_year
		fiscal_year = get_fiscal_year(self.posting_date, company=self.company)[0]

		gl_dict = frappe._dict({
			"company": self.company,
			"posting_date": self.posting_date,
			"fiscal_year": fiscal_year,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"remarks": args.get("remarks"),
			"account": args.get("account"),
			"against": args.get("against"),
			"debit": args.get("debit", 0),
			"credit": args.get("credit", 0),
			"debit_in_account_currency": args.get("debit_in_account_currency", 0),
			"credit_in_account_currency": args.get("credit_in_account_currency", 0),
			"party_type": args.get("party_type"),
			"cost_center": args.get("cost_center"),
			"party": args.get("party"),
			"is_opening": args.get("is_opening"),
		})

		return gl_dict

	def delete_gl_entries(self):

		gl_entries = frappe.get_all("GL Entry", filters={
			"voucher_type": self.doctype,
			"voucher_no": self.name
		})

		for gle in gl_entries:
			delete_doc("GL Entry", gle.name, ignore_permissions=True)

	def delete_payment_ledger_entries(self):

		payment_ledgers = frappe.get_all(
			"Payment Ledger Entry",
			filters={
				"voucher_type": "Loan Entry",
				"voucher_no": self.name,
				"party_type": "Employee",
				"party": self.loan_applicant,
			}
		)

		for ple in payment_ledgers:
			delete_doc("Payment Ledger Entry", ple.name, ignore_permissions=True)
@frappe.whitelist()
def get_expense_claim_account(expense_claim_type, company):
	account = frappe.db.get_value(
		"Expense Claim Account", {"parent": expense_claim_type, "company": company}, "default_account"
	)
	if not account:
		frappe.throw(
			_("Set the default account for the {0} {1}").format(
				frappe.bold(_("Expense Claim Type")),
				get_link_to_form("Expense Claim Type", expense_claim_type),
			)
		)

	return {"account": account}