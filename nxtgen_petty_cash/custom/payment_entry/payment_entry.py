import frappe

def custom_on_submit(doc, method):
    if doc.custom_petty_cash_fund:
        frappe.db.set_value("Petty Cash Fund", doc.custom_petty_cash_fund, "has_payment_entry", 1)
        