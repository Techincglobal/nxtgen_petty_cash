frappe.provide("erpnext.accounts");
frappe.ui.form.on("Petty Cash Fund", {
	refresh: function (frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Payment"), () => frm.events.make_payment_entry(frm), __("Create"));
			// frm.add_custom_button(__("Payment"), () => this.make_payment_entry(), __("Create"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Create"));

			// (
			// 	frm.doc.lead, () => {
			// 	// frappe.set_route("Form", "Lead", frm.doc.lead);
			// });
		}
	},
	make_payment_entry: function (frm) {
		return frappe.call({
			method: "nxtgen_petty_cash.nxtgen_petty_cash.doctype.petty_cash_fund.petty_cash_fund.make_payment_entry",
			args: {
				dt: frm.doc.doctype,
				dn: frm.doc.name,
			},
			callback: function (r) {
				var doc = frappe.model.sync(r.message);
				frappe.set_route("Form", doc[0].doctype, doc[0].name);
			},
		});
	},

});