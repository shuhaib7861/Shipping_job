// shipping_job.js
// Client logic for Shipping Job

frappe.ui.form.on("Shipping Job", {
    refresh(frm) {
        // show / hide land-only fields
        toggle_land_fields(frm);

        // auto-load invoices that have this Shipping Job set
        if (!frm.is_new()) {
            frm.call({
                method: "load_linked_invoices",   // method in shipping_job.py
                doc: frm.doc,
                callback() {
                    frm.refresh_field("invoices");
                    frm.refresh_field("total_invoice_amount");

                    // make child table read-only (no manual add / delete)
                    const grid = frm.get_field("invoices").grid;
                    grid.cannot_add_rows = true;
                    grid.cannot_delete_rows = true;
                    grid.refresh();
                }
            });
        }
    },

    job_type(frm) {
        toggle_land_fields(frm);
    }
});

function toggle_land_fields(frm) {
    const is_land = frm.doc.job_type === "Land";

    [
        "vehicle",
        "employee",
        "make_and_model",
        "place_of_loading",
        "place_of_delivery"
    ].forEach(df => {
        frm.toggle_display(df, is_land);
    });
}

