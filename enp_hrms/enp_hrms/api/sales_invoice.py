import frappe


@frappe.whitelist()
def get_last_sales_price(item_code, customer=None, current_invoice=None):

    conditions = [
        "sii.item_code = %(item_code)s"
    ]

    if customer:
        conditions.append("si.customer = %(customer)s")

    if current_invoice:
        conditions.append("si.name != %(current_invoice)s")

    condition_query = " AND ".join(conditions)

    result = frappe.db.sql(
        f"""
        SELECT
            sii.rate,
            si.name AS sales_invoice,
            si.posting_date
        FROM
            `tabSales Invoice Item` sii
        INNER JOIN
            `tabSales Invoice` si
            ON si.name = sii.parent
        WHERE
            {condition_query}
        ORDER BY
            si.posting_date DESC,
            si.creation DESC
        LIMIT 1
        """,
        {
            "item_code": item_code,
            "customer": customer,
            "current_invoice": current_invoice
        },
        as_dict=True
    )

    return result[0] if result else {}