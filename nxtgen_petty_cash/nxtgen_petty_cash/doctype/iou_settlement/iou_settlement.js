// Copyright (c) 2025, techincglobal and contributors
// For license information, please see license.txt

frappe.ui.form.on("IOU Settlement", {
	refresh(frm) {
		frm.set_query('iou_request', function () {
			return {
				filters: {
					'employee': frm.doc.employee
				}
			};
		});
	},
	return_amount: function (frm, cdt, cdn) {
		let expense_amount = 0;
		expense_amount = frm.doc.requested_amount - frm.doc.return_amount
		variance_amount = frm.doc.expected_return_amount - frm.doc.return_amount
		if(frm.doc.total_expenses<frm.doc.requested_amount){
			frm.set_value("expense_amount", expense_amount);
			frm.set_value("variance_amount", variance_amount);
		}else{
			frm.set_value("expense_amount", frm.doc.total_expenses);
		}

	},
	cal_total_expences(frm) {
		totel = 0
		frm.doc.expenses.forEach(line => {
			totel = totel + line.amount
		});
		frm.set_value("total_expenses", totel)
		if(frm.doc.total_expenses<frm.doc.requested_amount){

			frm.set_value("expected_return_amount",frm.doc.requested_amount-frm.doc.total_expenses)
		}else{

			frm.set_value("expected_return_amount",0)
			frm.set_value("return_amount",0)
			frm.set_value("additional_amount_requested",frm.doc.total_expenses-frm.doc.requested_amount)

		}
		// if frm.doc.
	}
});
frappe.ui.form.on('IOU Settlement Items', {
	amount(frm, cdt, cdn) {
		frm.trigger("cal_total_expences");
		// cal_total_expences(frm)
	}
	// cdt is Child DocType name i.e Quotation Item
	// cdn is the row name for e.g bbfcb8da6a
	// return_amount(frm, cdt, cdn) {
	//     let row = frappe.get_doc(cdt, cdn);
	// }
})
function cal_total_expences(frm) {
	totel = 0
	frm.doc.expenses.forEach(line => {
		totel = totel + line.amount
	});
	frm.set_value(total_expenses, totel)
}