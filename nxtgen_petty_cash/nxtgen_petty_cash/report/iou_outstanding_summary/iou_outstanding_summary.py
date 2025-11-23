# Copyright (c) 2025, techincglobal and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe import _
from frappe.utils import get_fullname

def execute(filters=None):
	columns = get_colums(filters)
	data =get_data(filters)
	return columns, data


def get_colums(filters=None):
	columns = [
		{
			"fieldname": "name",
			"label": _("IOU Request"),
			"fieldtype": "Link",
			"options": "IOU  Request",
		},
		{"fieldname": "petty_cash_box", "label": _("CashBox"), "fieldtype": "Link", "options": "Petty Cash Box"},
		{"fieldname": "department", "label": _("Department"), "fieldtype": "Link", "options": "Department"},
		{"fieldname": "date", "label": _("Requested Date"), "fieldtype": "Date"},
		{"fieldname": "approved_on", "label": _("Approved Date"), "fieldtype": "Date"},
		{"fieldname": "disbursed_on", "label": _("Disbursed Date"), "fieldtype": "Date"},
		{"fieldname": "employee_name", "label": _("Request By"), "fieldtype": "Data"},
		{"fieldname": "amount", "label": _("Request Amount"), "fieldtype": "Currency "},
		{"fieldname": "approved_ammount", "label": _("Approved Bxpended Amounty"), "fieldtype": "Currency"},
		{"fieldname": "disbursed_ammount", "label": _("Disbursed Amount"), "fieldtype": "Currency "},
	]
	return columns


def get_data(filters=None):
	conditions = "WHERE `tabIOU  Request`.docstatus=1 AND `tabIOU  Request`.`status` = 'Disbursed'"

	if filters.get("f_date") and filters.get("t_date"):
		conditions += f" AND DATE(`tabIOU  Request`.disbursed_on) BETWEEN '{filters.get('f_date')}' AND '{filters.get('t_date')}'"

	if filters.get("department"):
		conditions += f" AND `tabIOU  Request`.department = '{filters.get('department')}'"
	if filters.get("cash_box"):
		conditions += f" AND `tabIOU  Request`.petty_cash_box = '{filters.get('cash_box')}'"
	sql = f"""SELECT
		`tabIOU  Request`.`name`, 
	`tabIOU  Request`.employee, 
	`tabIOU  Request`.department, 
	`tabIOU  Request`.date, 
	`tabIOU  Request`.amount, 
	`tabIOU  Request`.approved_on, 
	`tabIOU  Request`.approved_ammount, 
	`tabIOU  Request`.disbursed_on, 
	`tabIOU  Request`.disbursed_ammount, 
	`tabIOU  Request`.petty_cash_box,
	tabEmployee.employee_name
FROM
	`tabIOU  Request`
 INNER JOIN
	tabEmployee
	ON
		`tabIOU  Request`.employee = tabEmployee.`name` {conditions}"""
	# frappe.throw(sql)
	row_data=frappe.db.sql(sql,as_dict=1)
	return row_data
