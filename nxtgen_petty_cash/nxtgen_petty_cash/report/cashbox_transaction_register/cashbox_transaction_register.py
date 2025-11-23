# Copyright (c) 2025, techincglobal and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe import _
from frappe.utils import get_fullname


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns(filters=None):
	columns = [
		{
			"fieldname": "name",
			"label": _("IOU Settlement"),
			"fieldtype": "Link",
			'options': 'IOU Settlement'
		},
		{"fieldname": "iou_request", "label": _("IOU Request"), "fieldtype": "Link",'options': 'IOU  Request'},
		{"fieldname": "cash_box", "label": _("CashBox"), "fieldtype": "Link",'options': 'Petty Cash Box'},
		{"fieldname": "department", "label": _("Department"), "fieldtype": "Link",'options': 'Department'},
		{"fieldname": "date", "label": _("Requested Date"), "fieldtype": "Date"},
		{"fieldname": "disbursed_on", "label": _("Disbursed Date"), "fieldtype": "Date"},
		{"fieldname": "settle_date", "label": _("Settle Date"), "fieldtype": "Date"},
		{"fieldname": "employee_name", "label": _("Request By"), "fieldtype": "Data"},
		{"fieldname": "requested_amount", "label": _("Disbursed Amount"), "fieldtype": "Currency "},
		{"fieldname": "total_expenses", "label": _("Expended Amount"), "fieldtype": "Currency "},
		{"fieldname": "additional_amount_requested", "label": _("Additional Bxpended Amounty"), "fieldtype": "Currency"},
	]
	return columns


def get_data(filters=None):
	conditions = "WHERE `tabIOU Settlement`.docstatus = 1"

	if filters.get("f_date") and filters.get("t_date"):
		conditions += f" AND DATE(`tabIOU Settlement`.settle_date) BETWEEN '{filters.get('f_date')}' AND '{filters.get('t_date')}'"

	if filters.get("department"):
		conditions += f" AND `tabIOU  Request`.department = \"{filters.get("department")}\""
	if filters.get("cash_box"):
		conditions += f" AND `tabIOU Settlement`.cash_box = \"{filters.get("cash_box")}\""

	# if filters.get("branch"):
	# 	conditions += f" AND `tabDocket Entry`.branch = \"{filters.get("branch")}\""

	sql = f"""SELECT
	`tabIOU Settlement`.`name`,
	`tabIOU Settlement`.requested_amount,
	`tabIOU Settlement`.iou_request,
	`tabIOU Settlement`.settle_date,
	`tabIOU Settlement`.total_expenses,
	`tabIOU Settlement`.additional_amount_requested,
	`tabIOU  Request`.department,
	`tabIOU  Request`.employee,
	tabEmployee.employee_name,
	`tabIOU  Request`.disbursed_on,
	`tabIOU  Request`.`date`,
	`tabIOU Settlement`.cash_box
FROM
	`tabIOU  Request`
	INNER JOIN
	`tabIOU Settlement`
	ON 
		`tabIOU  Request`.`name` = `tabIOU Settlement`.iou_request
	INNER JOIN
	tabEmployee
	ON 
		`tabIOU  Request`.employee = tabEmployee.`name` {conditions}"""
	row_data=frappe.db.sql(sql,as_dict=1)
	return row_data
