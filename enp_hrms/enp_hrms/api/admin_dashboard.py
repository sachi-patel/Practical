import frappe

def get_context(context):

    context.today_booking = frappe.db.count("service Booking",{"creation":[">=",frappe.utils.today()]})

    context.completed = frappe.db.count("Service Booking" ,{"status":"Completed"})

    context.pending = frappe.db.count("Service Booking",{"status":"Pending"})

    return context