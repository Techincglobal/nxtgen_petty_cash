// Copyright (c) 2025, techincglobal and contributors
// For license information, please see license.txt

frappe.ui.form.on("IOU  Request", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
            frm.page.set_indicator(frm.doc.status || "No Status", "blue");
		}
		frm.trigger("show_save_button");
		if (!frm.is_new()) {
			frm.add_custom_button(__('IOU Settlement'),
				function () {
					frm.trigger("make_iou_settlement")
				}, __('Create'));
		}
		//   frm.set_df_property("date", "min_date", frappe.datetime.get_today());
		// const day_datepicker = frm.fields_dict.date.datepicker;
		// day_datepicker.update({
		// 	minDate: frappe.datetime.str_to_obj(frappe.datetime.get_today())
		// 	// maxDate: frappe.datetime.str_to_obj(frm.doc.to_date),
		// });
	},
	employee: function (frm) {
		frm.trigger("set_approver");
	},
	set_approver: function (frm) {
		if (frm.doc.employee) {
			return frappe.call({
				method: "nxtgen_petty_cash.nxtgen_petty_cash.doctype.iou__request.iou__request.get_expences_approval",
				args: {
					employee: frm.doc.employee,
				},
				callback: function (r) {
					if (r && r.message) {
						frm.set_value("approver", r.message);
					}
				},
			});
		}
	},
	show_save_button: function (frm) {
		
		if (frm.doc.docstatus === 0) {
			$(".form-message").prop("hidden", true);
			if (frm.doc.status == "Pending") {

				frm.page.set_primary_action("Approve", () => {
					// console.log("Approve");
					let d = new frappe.ui.Dialog({
						title: 'Enter details',
						fields: [
							// {
							// 	label: 'First Name',
							// 	fieldname: 'first_name',
							// 	fieldtype: 'Data'
							// },
							
							{
								label: 'Approved Amount',
								fieldname: 'approved_amount',
								fieldtype: 'Currency',
								default: frm.doc.amount
							}
						],
						size: 'large', // small, large, extra-large 
						primary_action_label: 'Approve',
						primary_action(values) {
							frm.set_value('approved_ammount', values.approved_amount);
							frm.set_value('status', 'Approved');
							frm.set_value('approver', frappe.session.user);
							frm.set_value('approved_on', frappe.datetime.now_datetime());
							frm.save();
							console.log(values);
							d.hide();
						}
					});

					d.show();

					// frm.save();
				});
			}
			if (frm.doc.status == "Approved") {
			frm.page.set_primary_action("Disbursed", () => {
					// console.log("Approve");
					let d = new frappe.ui.Dialog({
						title: 'Enter details',
						fields: [
							// {
							// 	label: 'First Name',
							// 	fieldname: 'first_name',
							// 	fieldtype: 'Data'
							// },
							// {
							// 	label: 'Last Name',
							// 	fieldname: 'last_name',
							// 	fieldtype: 'Data'
							// },
							{
								label: 'Petty Cash Box',
								fieldname: 'petty_cash_box',
								fieldtype: 'Link',
								options: 'Petty Cash Box',
								reqd: 1,
							},

							{
								label: 'Disbursed Amount',
								fieldname: 'disbursed_amount',
								fieldtype: 'Currency',
								default: frm.doc.approved_ammount
							}
						],
						size: 'large', // small, large, extra-large 
						primary_action_label: 'Disbursed',
						primary_action(values) {
							d.hide();
							frm.set_value('disbursed_ammount', values.disbursed_amount);
							frm.set_value('petty_cash_box', values.petty_cash_box);
							frm.set_value('status', 'Disbursed');
							frm.set_value('disbursed_by', values.petty_cash_box);
							frm.set_value('disbursed_by', frappe.session.user);
							frm.set_value('disbursed_on', frappe.datetime.now_datetime());
							frm.save();
							frm.submit();
							// console.log(values);
							
						}
					});

					d.show();

					// frm.save();
				});
			}
			// frm.page.set_primary_action("Save", () => {
			// 	frm.save();
			// });
		}


	},
	make_iou_settlement:function(frm){
		frappe.model.open_mapped_doc({
			method: "nxtgen_petty_cash.nxtgen_petty_cash.doctype.iou__request.iou__request.make_iou_settlement",
			frm: frm
		})
	}
});
