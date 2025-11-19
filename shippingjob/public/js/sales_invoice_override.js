// shippingjob/shippingjob/public/js/sales_invoice_override.js

function make_due_date_optional(frm) {
    // turn off required in all the places Frappe uses
    frm.set_df_property("due_date", "reqd", 0);
    frm.toggle_reqd("due_date", false);

    if (frm.fields_dict && frm.fields_dict.due_date) {
        frm.fields_dict.due_date.df.reqd = 0;
        frm.fields_dict.due_date.refresh();
    }
}

function make_due_date_optional_delayed(frm) {
    // run AFTER ERPNext's own handlers (customer / payment terms)
    setTimeout(() => {
        make_due_date_optional(frm);
    }, 50);
}

frappe.ui.form.on("Sales Invoice", {
    onload(frm) {
        make_due_date_optional_delayed(frm);
    },
    refresh(frm) {
        make_due_date_optional_delayed(frm);
    },
    customer(frm) {
        make_due_date_optional_delayed(frm);
    },
    payment_terms_template(frm) {
        make_due_date_optional_delayed(frm);
    },
    validate(frm) {
        // just before save, make 100% sure it's not required
        make_due_date_optional(frm);
    }
});
