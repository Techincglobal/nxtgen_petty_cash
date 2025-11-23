# Copyright (c) 2025, techincglobal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint, comma_or, flt, getdate, nowdate
from frappe.model.mapper import get_mapped_doc


class IOURequest(Document):
	# pass
	def on_insert(self):
		self.status="Pending"
		self.send_notification()
	def on_submit(self):
		petty_cash_ledger = frappe.get_doc({
			'doctype': 'Petty cash Ledger',
			'date': getdate(),
			'petty_cash_box': self.petty_cash_box,
			'voucher_type':self.doctype,
			'voucher_no': self.name,
			'expense_category': self.expenses_type,
			'transaction_type':"Payment",
			'paid_cr':self.disbursed_ammount
		})
		petty_cash_ledger.insert(ignore_permissions=True)

	def send_notification(self):
		pass

@frappe.whitelist()
def get_expences_approval(employee):
	approval = frappe.db.get_value("Employee", employee, "expense_approver")
	return approval
@frappe.whitelist()
def make_iou_settlement(source_name, target_doc=None, args=None):
	# from erpnext.stock.doctype.packed_item.packed_item import make_packing_list
	if args is None:
		args = {}
	if isinstance(args, str):
		args = json.loads(args)

	def set_missing_values(source, target):
		pass
		# total_cbm = 0
		# total_net_weight = 0
		# total_no_of_cartons = 0
		# total_qty_in_pcs = 0
		# total_shipped = 0
		# total_gross_weight = 0
		# total_packing_net_weight = 0
		# total_packing_gross_weight = 0		
		# for d in target.package_lines:
		# 	total_cbm = total_cbm + d.cbm
		# 	total_net_weight = total_net_weight + flt(d.net_weight)
		# 	total_no_of_cartons = total_no_of_cartons + flt(d.no_of_cartons)
		# 	total_qty_in_pcs = total_qty_in_pcs+flt(d.no_of_pcs)
		# 	total_shipped = total_shipped + flt(d.qty_packing_units)
		# 	total_gross_weight = total_gross_weight + flt(d.gross_weight)
		# 	total_packing_net_weight = total_packing_net_weight + \
		# 		flt(d.packing_net_weight)
		# 	total_packing_gross_weight = total_packing_gross_weight + \
		# 		flt(d.packing_gross_weight)		
		# target.run_method("set_missing_valu
		# target.total_cbm=len(target.cpo_lines)
		# target.destination_country==d.
		# target.total_cbm = total_cbm
		# target.total_net_weight = total_net_weight
		# target.total_no_of_cartons = total_no_of_cartons
		# target.total_qty_in_pcs = total_qty_in_pcs
		# target.total_shipped = total_shipped
		# target.total_gross_weight = total_gross_weight
		# target.total_net_weight_pre = total_packing_net_weight
		# target.total_gross_weight_pre = total_packing_gross_weight
		# target.run_method("set_missing_values")
		# target.run_method("set_po_nos")
		# target.run_method("calculate_taxes_and_totals")		
		# if source.company_address:
		# 	target.update({"company_address": source.company_address})
		# else:
		# 	# set company address
		# 	target.update(get_company_address(target.company))		
		# if target.company_address:
		# 	target.update(get_fetch_values("Delivery Note", "company_address", target.company_address))		
		# make_packing_list(target)

	def update_item(source, target, source_parent):
		pass
	# 	if not target.color_description:
	# 		sql = f"""SELECT
	# `tabCargo Advice Group Lines`.color_description
    # FROM
	# `tabPreshipment Lines`
	# INNER JOIN
	# `tabCargo Advice Group Lines`
	# ON 
	# 	`tabPreshipment Lines`.style_no = `tabCargo Advice Group Lines`.style_no AND
	# 	`tabPreshipment Lines`.color_code = `tabCargo Advice Group Lines`.color_code AND
	# 	`tabPreshipment Lines`.buyer_style_no = `tabCargo Advice Group Lines`.buyer_style_no AND
	# 	`tabPreshipment Lines`.customer_purchase_order_number = `tabCargo Advice Group Lines`.customer_purchase_order_number
    # WHERE
	# `tabPreshipment Lines`.`name` = '{source.name}'"""
    #         color_description = frappe.db.sql(sql, as_dict=True)   
    #         target.color_description = color_description[0].color_description if color_description else ''
        # target.base_amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.base_rate)
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

	mapper = {
		"IOU  Request": {"doctype": "IOU Settlement", "validation": {"docstatus": ["=", 1]},
				"field_map": {
				# "iou_request": source_name,
    			"disbursed_ammount":"requested_amount",
				'petty_cash_box':'cash_box'
       },
		},
		# "Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
		# "Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
	}
    # args
	skip_item_mapping = False
	if not skip_item_mapping:

		def condition(doc):
			if (args.get("allow_child_item_selection")) == 1:
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

		# mapper["Preshipment Lines"] = {
		# 		"doctype": "Package Update Lines",
		# 		"field_map": {
		# 		"order_qty": "order_qty",
		# 		"net_weight": "packing_net_weight",
		# 		"gross_weight": "packing_gross_weight",
		# 		"to_be_shipped_qty": "qty_packing_units"
		# 		# "order_no":"customer_order"

		# 	},
		# 	"postprocess": update_item,
		# 	"condition": condition,
		# }

	target_doc = get_mapped_doc(
		"IOU  Request", source_name, mapper, target_doc, set_missing_values)
	# target_doc.run_method("set_totals")
	# target_doc.set_onload("ignore_price_list", True)

	return target_doc
