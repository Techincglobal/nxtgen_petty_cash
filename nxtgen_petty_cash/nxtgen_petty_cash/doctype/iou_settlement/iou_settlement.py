# Copyright (c) 2025, techincglobal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint, comma_or, flt, getdate, nowdate
from frappe.model.mapper import get_mapped_doc

class IOUSettlement(Document):
	# pass
	def on_submit(self):
		on_submition_validation(self)
		frappe.db.set_value("IOU  Request", self.iou_request, "status", "Settled")

		petty_cash_box	= frappe.db.get_value("IOU  Request", self.iou_request, "petty_cash_box")
		make_petty_cash_log(self,petty_cash_box)
	def on_cancel(self):
		frappe.db.set_value("IOU  Request", self.iou_request, "status", "Disbursed")
		log_list=frappe.db.get_list('Petty cash Ledger',
    		filters={
        		'voucher_type': self.doctype,
				'voucher_no':self.name
    		},pluck='name')
		for log in log_list:
			frappe.db.set_value('Petty cash Ledger', log, 'is_cancel', 1)

def on_submition_validation(doc):
	if doc.requested_amount>doc.total_expenses:
		if doc.return_amount!=doc.expected_return_amount:
			frappe.throw(
                "Actual Return and Expected Return must match when changed."
            )
def make_petty_cash_log(doc,petty_cash_box):
	if doc.requested_amount>doc.total_expenses:
		if doc.return_amount>0:
			petty_cash_ledger = frappe.get_doc({
				'doctype': 'Petty cash Ledger',
				'date': doc.settle_date,
				'petty_cash_box': petty_cash_box,
				'voucher_type':doc.doctype,
				'voucher_no': doc.name,
				'transaction_type':"Receipt",
				'received_dr':doc.return_amount
			})
			petty_cash_ledger.insert(ignore_permissions=True)
	else:
		if doc.additional_amount_requested>0:
			petty_cash_ledger = frappe.get_doc({
				'doctype': 'Petty cash Ledger',
				'date': doc.settle_date,
				'petty_cash_box': petty_cash_box,
				'voucher_type':doc.doctype,
				'voucher_no': doc.name,
				'transaction_type':"Receipt",
				'paid_cr':doc.additional_amount_requested
			})
			petty_cash_ledger.insert(ignore_permissions=True)
@frappe.whitelist()
def make_petty_cas_pay(source_name, target_doc=None,args=None):
	if args is None:
		args = {}
	if isinstance(args, str):
		args = json.loads(args)
	def set_missing_values(source, target):
		# pass
		total=0
		for d in target.items:
			total=total+d.amount
		target.total=total
		# total_net_weight = 0
		# total_no_of_cartons = 0
		# total_qty_in_pcs = 0
		# total_shipped = 0
		# total_gross_weight = 0
		# for d in target.cpo_lines:
		# 	total_cbm = total_cbm + d.cbm
		# 	total_net_weight = total_net_weight + flt(d.net_weight)
		# 	total_no_of_cartons = total_no_of_cartons + flt(d.no_of_cartons)
		# 	total_qty_in_pcs = total_qty_in_pcs+flt(d.no_of_pcs)
		# 	total_shipped = total_shipped + flt(d.to_be_shipped_qty)
		# 	total_gross_weight = total_gross_weight + flt(d.gross_weight)

		# # target.run_method("set_missing_valu
		# # target.total_cbm=len(target.cpo_lines)
		# target.destination_country=source.cargo_advice_lines[0].destination_country
		# target.mode_of_shipment=source.cargo_advice_lines[0].shipment_mode
		# target.total_cbm=total_cbm
		# target.total_net_weight=total_net_weight
		# target.total_no_of_cartons=total_no_of_cartons
		# target.total_qty_in_pcs= total_qty_in_pcs
		# target.total_shipped=total_shipped
		# target.total_gross_weight=total_gross_weight
		# # target.run_method("set_missing_values")
		# # target.run_method("set_po_nos")
		# # target.run_method("calculate_taxes_and_totals")

		# # if source.company_address:
		# # 	target.update({"company_address": source.company_address})
		# # else:
		# # 	# set company address
		# # 	target.update(get_company_address(target.company))

		# # if target.company_address:
		# # 	target.update(get_fetch_values("Delivery Note", "company_address", target.company_address))

		# # make_packing_list(target)

	def update_item(source, target, source_parent):
		# pass
		target.iou_request=source_parent.iou_request
		# target.value =  (flt(source.to_be_shipped_qty)* flt(source.unit_price))- flt(source.commission_amount) 
		# target_parent.total_cbm=100
		# target.amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.rate)
		# target.qty = flt(source.qty) - flt(source.delivered_qty)

		# item = get_item_defaults(target.item_code, source_parent.company)
		# item_group = get_item_group_defaults(target.item_code, source_parent.company)

		# if item:
		# 	target.cost_center = (
		# 		frappe.db.get_value("Project", source_parent.project, "cost_center")
		# 		or item.get("buying_cost_center")
		# 		or item_group.get("buying_cost_center")
		# 	)
	def update_totals(source, target, source_parent):
		target.total_cbm=len(target.cpo_lines)

	mapper = {
		"IOU Settlement": {
			"doctype": "Petty Cash Payment Entry", 
			"validation": {"docstatus": ["=", 1]},
			# "field_map": {
			# 	"buy": "buy",
			# },
			# # "postprocess": update_totals,
			},
		# "Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
		# "Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
	}
	# args
	skip_item_mapping=False
	if not skip_item_mapping:
		
		def condition(doc):
			if(args.get("allow_child_item_selection"))==1:
				filtered_items = args.get("filtered_children", [])
				# if len(filtered_items)>0:
				if doc.name in filtered_items:
					return True
				else:
					return False
			else:
				return True
			
			# make_mapped_doc sets js `args` into `frappe.flags.args`
			# if frappe.flags.args and frappe.flags.args.delivery_dates:
			# 	if cstr(doc.delivery_date) not in frappe.flags.args.delivery_dates:
			# 		return False
			# return abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier != 1

		mapper["IOU Settlement Items"] = {
			"doctype": "Petty Cash Payment Entry Item",
			"field_map": {
				"expenses_type":'claim_type',
				"amount":"amount",
				"descriptions":"description"
				# "buy": "buy",
				# "cmb":"cbm",
				# 'qty_in_pieces':"no_of_pcs",
				# 'fabrication':"fabric_content",
				#  "item_descriptions":"item_name_logistics"
				# "destination_country":
				# "order_no":"customer_order"
				
			},
			"postprocess": update_item,
			"condition": condition,
		}

	target_doc = get_mapped_doc("IOU Settlement", source_name, mapper, target_doc, set_missing_values)

	# target_doc.set_onload("ignore_price_list", True)

	return target_doc