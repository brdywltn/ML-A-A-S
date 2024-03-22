import paypalrestsdk
from django.conf import settings
from django.http import JsonResponse

def create_payment(request):
    # Configure PayPal SDK
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET  
    })

    # Create payment object
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": "",
            "cancel_url": "",
        },
        "transactions" : [{
            "item_list" : {
                "items" : [{
                    "name": "Test item",
                    "sku": "test item",
                    "price": "9.99",
                    "currency": "GBP",
                    "quantity": 1,
                }]
            },
            "amount" : {
                "total": "9.99",
                "currency": "GBP"
            },
            "description": "Test payment description"
        }]
    })

    if payment.create():
        print("Payment created successfully!")
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                print("Redirect for approval: %s" % (approval_url))
                return JsonResponse({"approval_url": approval_url})
    else:
        print(payment.error)
    return JsonResponse({"error": "Payment creation failed"})

def execute_payment(request):
    pass