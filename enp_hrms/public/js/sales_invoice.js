frappe.ui.form.on("Sales Invoice Item", {

    item_code(frm, cdt, cdn) {
        show_price_history(frm, cdt, cdn);
    },

    form_render(frm, cdt, cdn) {
        show_price_history(frm, cdt, cdn);
    }
});


async function show_price_history(frm, cdt, cdn) {

    let row = locals[cdt][cdn];

    if (!row.item_code) return;

    let r = await frappe.call({
        method: "enp_hrms.enp_hrms.api.sales_invoice.get_last_sales_price",
        args: {
            item_code: row.item_code,
            customer: frm.doc.customer || "",
            current_invoice: frm.doc.name || ""
        }
    });

    let data = r.message;

    console.log("DATA =>", data);

    let html = "";

    if (data && data.sales_invoice) {

        html = `
            <div style="
                padding:10px;
                background:#f8f9fa;
                border:1px solid #d1d8dd;
                border-radius:6px;
                margin-top:5px;
            ">

                <div>
                    <b>Last Price:</b> ₹ ${data.rate}
                </div>

                <div>
                    <b>Invoice:</b>
                    <a href="/app/sales-invoice/${data.sales_invoice}"
                       target="_blank">
                        ${data.sales_invoice}
                    </a>
                </div>

                <div>
                    <b>Date:</b> ${data.posting_date}
                </div>

            </div>
        `;

    } else {

        html = `
            <div style="
                color:gray;
                padding:8px;
            ">
                No previous sales history
            </div>
        `;
    }

    setTimeout(() => {

        let grid_row = frm.fields_dict.items.grid.get_row(cdn);

        if (!grid_row) {
            console.log("Grid row not found");
            return;
        }

        grid_row.toggle_view(true);

       
        setTimeout(() => {

            if (
                grid_row.grid_form &&
                grid_row.grid_form.fields_dict &&
                grid_row.grid_form.fields_dict.custom_price_history
            ) {

                $(grid_row.grid_form.fields_dict.custom_price_history.wrapper)
                    .html(html);

            } else {

                console.log("HTML field not found");
            }

        }, 200);

    }, 300);
}