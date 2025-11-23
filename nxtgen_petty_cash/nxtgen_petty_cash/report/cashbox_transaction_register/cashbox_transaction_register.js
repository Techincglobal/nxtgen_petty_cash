// Copyright (c) 2025, techincglobal and contributors
// For license information, please see license.txt

frappe.query_reports["Cashbox Transaction Register"] = {
	"filters": [
			{
			"fieldname": "cash_box",
			"label": __("CashBox"),
			"fieldtype": "Link",
			"options": "Petty Cash Box"
		},
		
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "f_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default":  frappe.datetime.month_start()
		},
		{
			"fieldname": "t_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
	]
};
