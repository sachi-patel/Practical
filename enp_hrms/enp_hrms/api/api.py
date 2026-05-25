import frappe

@frappe.whitelist(allow_guest=True)
def create_booking(customer_name,category,latitude,longitude):
    providers = frappe.get_all("Service Provider",{"available":1},["name","rating","latitude","longitude"])
    best_provider = None
    best_score = 999999

    for p in providers:
        distance =(abs(float(latitude)-float(p.latitude)) + abs(float(longitude) - float(p.longitide)))
        score = distance - float(p.rating)

        if score < best_score:
            best_score = score 
            best_provider = p

    booking = frappe.get_doc({
        "doctype" :"Service Booking",
        "customer_name": customer_name,
        "service_category":category,
        "assigned_provider":best_provider.name if best_provider else None,
        "distance" : best_score,
        "status" : "Assigned"
    })

    booking.insert()

    frappe.sendmail(
        recipients=["admin@example.com"],
        subject="Booking Created",
        message=f"Booking {booking.name} created."
    )

    return booking.name

@frappe.whitelist()
def get_available_providers(location):
    return frappe.get_all("Service Provider",{"location":location,"available":1},["name","rating"])


@frappe.whitelist()
def accept_booking(booking_id):
    booking = frappe.get_doc("Service Booking",booking_id)
    booking_status = "Accepted"
    booking.save()

    return "Booking Accepted"


@frappe.whitelist()
def booking_status(booking_id):
    booking = frappe.get_doc("Service Booking",booking_id)
    return {
        "status": booking.status,
        "provider": booking.assigned_provider,
        "price": booking.price
    }














