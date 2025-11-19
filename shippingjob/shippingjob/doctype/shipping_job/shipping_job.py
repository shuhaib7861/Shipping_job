# shipping_job.py

import frappe
from frappe.model.document import Document

class ShippingJob(Document):

    def validate(self):
        # for Land jobs, ensure vehicle-related things make sense (optional)
        self.set_vehicle_details()
        # always keep total in sync on server side as well
        self.set_total_invoice_amount()

    # ---------- Vehicle details ----------
    def set_vehicle_details(self):
        if self.job_type != "Land" or not self.vehicle:
            return

        vehicle = frappe.db.get_value(
            "Vehicle",
            self.vehicle,
            ["employee", "make"],   # make sure these fieldnames exist on Vehicle
            as_dict=True,
        )

        if vehicle:
            self.employee = vehicle.employee
            self.make_and_model = vehicle.make

    # ---------- Sum of invoices (only submitted, from Sales Invoice.shipping_job) ----------
    def set_total_invoice_amount(self):
        """Set Total Invoice Amount from all submitted Sales Invoices
        that have this Shipping Job in their `shipping_job` field.
        """
        if not self.name:
            self.total_invoice_amt = 0
            return

        invoices = frappe.get_all(
            "Sales Invoice",
            filters={
                "custom_shipping_job": self.name,
                "docstatus": 1,  # only submitted invoices
            },
            fields=["grand_total"],
        )

        total = sum((inv.grand_total or 0) for inv in invoices)
        self.total_invoice_amt = total

    # ---------- Fill child table from Sales Invoice ----------
    @frappe.whitelist()
    def load_linked_invoices(self):
        """Populate child table with all submitted Sales Invoices
        that have this Shipping Job in their `shipping_job` field.
        Used from shipping_job.js on refresh.
        """
        if not self.name:
            return

        invoices = frappe.get_all(
            "Sales Invoice",
            filters={
                "custom_shipping_job": self.name,
                "docstatus": 1,
            },
            fields=["name", "customer", "posting_date", "grand_total"],
        )

        # clear current child table and refill
        self.set("invoices", [])

        total = 0
        for inv in invoices:
            self.append("invoices", {
                "sales_invoice": inv.name,
                "customer": inv.customer,
                "posting_date": inv.posting_date,
                "amount": inv.grand_total,
            })
            total += inv.grand_total or 0

        self.total_invoice_amount = total

        # return something for JS if needed
        return {
            "total": total,
            "count": len(invoices),
        }
