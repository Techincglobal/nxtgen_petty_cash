import frappe

def custom_customer_naming(doc, method):
    # Get first letter of customer name
    first_letter = doc.customer_name[0].upper() if doc.customer_name else "C"

    # Generate a series number
    # You can change the series key 'CUST-' to anything
    series_number = frappe.model.naming.make_autoname(f"{first_letter}-.#####")

    # If customer currency is USD, add postfix
    if doc.custom_currency == "USD":
        series_number = f"{series_number}-USD"

    # Set the name
    doc.name = series_number