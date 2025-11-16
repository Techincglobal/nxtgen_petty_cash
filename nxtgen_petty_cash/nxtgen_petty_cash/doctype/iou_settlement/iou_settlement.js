// Copyright (c) 2025, techincglobal and contributors
// For license information, please see license.txt

frappe.ui.form.on("IOU Settlement", {
	refresh(frm) {
	},
	return_amount: function (frm, cdt, cdn) {
		let expense_amount = 0;
		expense_amount =frm.doc.requested_amount-frm.doc.return_amount
		frm.set_value("expense_amount", expense_amount);
	}
});	