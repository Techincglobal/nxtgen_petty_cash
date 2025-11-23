frappe.provide("erpnext.accounts");
frappe.ui.form.on("Petty Cash Fund", {
	refresh: function (frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Payment"), () => frm.events.make_payment_entry(frm), __("Create"));
			// frm.add_custom_button(__("Payment"), () => this.make_payment_entry(), __("Create"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Create"));
			frm.trigger("make_dashboard");
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
	petty_cash_box: function (frm) {
		frm.trigger("make_dashboard");
	},
	make_dashboard: function (frm) {
		// erpnext.utils.render_dashboard({
		// 	parent: frm,
		// 	title: __("Petty Cash Fund Dashboard"),
		// 	data: frm.dashboard_data
		// });
		$("div").remove(".form-dashboard-section.custom");
		frappe.call({
			method: "frappe.client.get", // The server-side method to call
			args: {
				doctype: "Petty Cash Box", // Replace with the actual DocType name
				name: frm.doc.petty_cash_box, // Replace with the specific document's name/ID
			},
			callback: function (r) {
				if (r.message) {
					var doc = r.message; // The retrieved document object
					console.log(doc);
					frm.dashboard.add_section(
						frappe.render_template("petty_cash_fund_dashboard", {
							data: {"avl_bal_amount": doc.balance_amount,"oustanding_amount": doc.outstanding_amount,"flot_ammount":doc.floating_amount},
						})
						,
						__("Cash Box Details"),
					);
				} else {
					console.error("Error retrieving document:", r);
				}
			}
		});


		// "<div class='dashboard-section custom'>\n\
		// <div class='dashboard-item'>\n\
		// 	<div class='dashboard-item-value'>"+1+"</div>\n\
		// 	<div class='dashboard-item-label'>Total Amount</div>\n\
		// </div>\n\
		// </div>"

		frm.dashboard.show();
	}

});