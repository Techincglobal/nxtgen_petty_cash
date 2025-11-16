# Copyright (c) 2025, techincglobal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IOUSettlement(Document):
	pass
	# def on_submit(self):
	# 	frappe.db.set_value("IOU Request", self.iou_request, "status", "Settled")