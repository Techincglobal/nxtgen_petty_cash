// Copyright (c) 2025, techincglobal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Petty Cash Payment Entry", {
	refresh(frm) {
		frm.events.show_general_ledger(frm);
		erpnext.accounts.ledger_preview.show_accounting_ledger_preview(frm);

		frm.add_custom_button(__('IOU Settlement'), function () {
			if (!frm.doc.petty_cash_box) {
				frappe.throw({
					title: __("Mandatory"),
					message: __("You must select a Cashbox before continuing.")
				});
			}
			// if (frm.doc.petty_cash_box) {
			// 	frappe.throw("You must select a Cashbox before continuing.")
			// }
			new frappe.ui.form.MultiSelectDialog({
				doctype: "IOU Settlement",
				target: cur_frm,
				setters: {
					iou_request: null,
					settle_date: null,
					total_expenses: null,
					// cash_box:frm.doc.petty_cash_box
				},
				// read_only_setters:{
				// 	
				// },
				add_filters_group: 1,
				size: 'large', // small, large, extra-large
				date_field: "settle_date",
				allow_child_item_selection: true,
				child_fieldname: "expenses", // child table fieldname, whose records will be shown &amp; can be filtered
				child_columns: ["expenses_type", "descriptions", "amount"], // child item columns to be displayed
				// date_field: "transaction_date",
				get_query() {
					return {
						filters: {
							docstatus: 1,
							is_gl_done: 0,
							cash_box:frm.doc.petty_cash_box

						}
					}
				},
				action(selections, args1) {
					// console.log(selections,args1);
					// console.log(args1.filtered_children)
					// opts.source_name=selections
					if (selections.length === 0) {
						
							frappe.msgprint(__("Please select {0}", ["IOU Settlement"]))
						return;
					}
					frappe.call({
						// Sometimes we hit the limit for URL length of a GET request
						// as we send the full target_doc. Hence this is a POST request.
						type: "POST",
						method: 'frappe.model.mapper.map_docs',
						// method: "erpnext.logistics.doctype.cargo_advice.cargo_advice.make_preshipment",
						args: {
							"method": "nxtgen_petty_cash.nxtgen_petty_cash.doctype.iou_settlement.iou_settlement.make_petty_cas_pay",
							"source_names": selections,
							"target_doc": cur_frm.doc,
							"skip_item_mapping": false,
							// selected_lins:args1.filtered_children,
							"args": args1,
						},
						callback: function (r) {
							if (!r.exc) {
								var doc = frappe.model.sync(r.message);
								cur_frm.dirty();
								// cur_frm.refresh();
								refresh_field("cpo_lines");
								refresh_field("total_cbm");
								cur_frm.refresh_fields()
								cur_dialog.hide();
								// cur_frm.save();
								// var total_cbm = 0
								// var total_net_weight = 0
								// var total_no_of_cartons = 0
								// var total_qty_in_pcs = 0
								// var total_shipped = 0
								// var total_gross_weight = 0
								// console.log(cur_frm.doc.cpo_lines)
								// // cur_frm.doc.cpo_lines.forEach(d => {
								// 	$.each(frm.doc.cpo_lines || [], function(i, d) {
								// 	console.log(d)
								// 	total_cbm = total_cbm + d.cbm
								// 	total_net_weight = total_net_weight + d.net_weight
								// 	total_no_of_cartons = total_no_of_cartons + d.no_of_cartons
								// 	total_qty_in_pcs = total_qty_in_pcs.d.no_of_pcs
								// 	total_shipped = total_shipped + d.to_be_shipped_qty
								// 	total_gross_weight = total_gross_weight + d.gross_weight

								// });
								// console.log(cur_frm)
								// // cur_frm.set_value('total_cbm', total_cbm)
								// // frappe.model.set_value(cur_frm.doctype, cur_frm.name, 'total_cbm', total_cbm)
								// // frappe.model.set_value(cur_frm.doctype, cur_frm.name, 'total_net_weight', total_net_weight)
								// // frappe.model.set_value(cur_frm.doctype, cur_frm.name, 'total_no_of_cartons', total_no_of_cartons)
								// // frappe.model.set_value(cur_frm.doctype, cur_frm.name, 'total_qty_in_pcs', total_qty_in_pcs)
								// // frappe.model.set_value(cur_frm.doctype, cur_frm.name, 'total_shipped', total_shipped)
								// // frappe.model.set_value(cur_frm.doctype, cur_frm.name, 'total_gross_weight', total_gross_weight)
								// cur_frm.refresh_fields()
								// // refresh_field("total_cbm")
								// // refresh_field("total_net_weight")
								// // refresh_field("total_no_of_cartons")
								// // refresh_field("total_qty_in_pcs")
								// // refresh_field("total_shipped")
								// // refresh_field("total_gross_weight")

								// // console.log(cur_frm)
							}
						}
					});
				}
			});
		}, __("Get Items From"));
	},

	calculate_total_amount(frm) {
		let total = 0;
		frm.doc.items.forEach((item) => {
			total += item.amount;
		});
		frm.set_value("total", total);
	},
	show_general_ledger: function (frm) {
		if (frm.doc.docstatus > 0) {
			frm.add_custom_button(
				__("Ledger"),
				function () {
					frappe.route_options = {
						voucher_no: frm.doc.name,
						from_date: frm.doc.posting_date,
						to_date: moment(frm.doc.modified).format("YYYY-MM-DD"),
						company: frm.doc.company,
						categorize_by: "",
						show_cancelled_entries: frm.doc.docstatus === 2,
					};
					frappe.set_route("query-report", "General Ledger");
				},
				"fa fa-table"
			);
		}
	},
});
frappe.ui.form.on('Petty Cash Payment Entry Item', {
	// cdt is Child DocType name i.e Quotation Item
	// cdn is the row name for e.g bbfcb8da6a
	amount(frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		calculate_total_amount(frm);
	},
	items_add(frm, cdt, cdn) {
		console.log("Item added");
		// let row = frappe.get_doc(cdt, cdn);
		// row.amount = row.quantity * row.rate;
		frm.refresh_field("items");
		frm.trigger("calculate_total_amount");
	},
	items_remove(frm, cdt, cdn) {
		console.log("Item removed");
		frm.trigger("calculate_total_amount");
	},
	items_change(frm, cdt, cdn) {
		console.log("Item changed");
		// let row = frappe.get_doc(cdt, cdn);
		// row.amount = row.quantity * row.rate;
		frm.refresh_field("items");
		frm.trigger("calculate_total_amount");
	},
})

function calculate_total_amount(frm) {
	let total = 0;
	frm.doc.items.forEach((item) => {
		total += item.amount;
	});
	frm.set_value("total", total);
}