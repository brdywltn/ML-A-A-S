import paypalrestsdk
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import redirect, render
from django.urls import reverse
from .views import get_log_data, create_log
from .models import UserTokenCount, Action
from rest_framework.response import Response
from rest_framework import status

# Create a payment that can be made via the PayPal API
def create_payment(request, purchase_type):
    # Configure PayPal SDK
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

    # We need to check what kind of payment it is first, how many tokens are being bought?
    if purchase_type == "single":
        name = "Single purchase"
        sku = "sku01"
        quantity = 1
        price = "9.99"
        description = "Single purchase of 1 token"

    elif purchase_type == "bulk":
        name = "Bulk purchase"
        sku = "sku02"
        quantity = 10
        price = "44.99"
        description = "Bulk purchase of 10 tokens"
    else:
        return JsonResponse({"error": "Invalid purchase type"})

    # Pass the quantity to the session to later change the payment execution type
    request.session['purchase_quantity'] = quantity 
    
    # Create payment object
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_cancelled')),
        },
        "transactions" : [{
            "item_list" : {
                "items" : [{
                    "name": name,
                    "sku": sku,
                    "price": price,
                    "currency": "GBP",
                    "quantity": 1,
                }]
            },
            "amount" : {
                "total": price,
                "currency": "GBP"
            },
            "description": description
        }]
    })

    # Successfully communicated with API
    if payment.create():
        print("Payment created successfully!")
        # get url for payment approval
        for link in payment.links:
            if link.rel == "approval_url":
                # turn link into text
                approval_url = str(link.href)
                # send on merry way
                return redirect(approval_url)
    else:
        print(payment.error)


# Execute a successful payment
def execute_payment(request):
    # Get payment id and payer id
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    #If neither ID, error, restart
    if not payment_id or not payer_id:
        print("no payment id or payer_id")
        return Response({"error": "Error: No payment id or payer id was found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # configure API
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

    # Check we've got a successful payment
    payment = paypalrestsdk.Payment.find(payment_id)

    # If it we do an the payer IDs match
    if payment.execute({"payer_id": payer_id}):
        print("Payment executed successfully!")
        print(f"Payment: {payment}")

        # Allocate some tokens
        tokens_purchased = request.session.get("purchase_quantity")

        add_tokens(request.user, tokens_purchased)
        # log_data = {
        #     'action': 'Tokens purchased',

        # }
        log_data = get_log_data(request.user, Action.PAYMENT_SUCCESSFUL, 'success', description=f"Purchased {tokens_purchased} tokens")
        create_log(request.user if request.user.is_authenticated else None, log_data)


        return redirect('success')
    else:
        print("exiting at the end of execute_payment(), incorrect payer id")
        return Response({"error": "Error: Payment failed to execute, incorrect payer id"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def add_tokens(user, tokens):
    token_count_instance, created = UserTokenCount.objects.get_or_create(user=user)
    token_count_instance.token_count += int(tokens)
    token_count_instance.save()
    
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

def payment_success(request):
    log_data = get_log_data(request.user, Action.PAYMENT_SUCCESSFUL, 'success')
    create_log(request.user, log_data)
    return render(request,'payment_success.html')
