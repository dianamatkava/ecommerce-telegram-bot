import os
import requests
from dotenv import load_dotenv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, PaymentAddress, GiftOrder
from .utils import get_fiat_amount


load_dotenv()


@csrf_exempt
def home(request):
    if request.method == 'POST':
        URL = os.getenv('TEST_PAYPAL_IPN') #'PAYPAL_IPN', 
        params = {'cmd': '_notify-validate'}
        params.update(request.POST.dict())
        response = requests.post(URL, params=params)

        if response.text == 'VERIFIED':
            amount = request.POST.get('mc_gross')
            status = request.POST.get('payment_status', False)
            payer_email = request.POST.get('payer_email')
            currency = request.POST.get('mc_currency')
            receiver_email = request.POST.get('receiver_email')
            payment_date = request.POST.get('payment_date')
            print(request.POST.__dict__)
            
            if status == 'Completed':
                user = None
                fiat_amount = None
                order = GiftOrder.objects.filter(
                    TxID=payer_email
                )
                if not order:
                    order = None
                else:
                    user = order.user
                    if currency != order.offer.buy_cur:
                        fiat_amount = get_fiat_amount(
                            order.offer.buy_cur, currency, amount
                        )
                
                address = PaymentAddress.objects.filter(
                    address=receiver_email
                ) 
                if not address:
                    address = None

                payment = Payment.objects.create(
                    TxID=payer_email,
                    amount=amount,
                    address=address[0],
                    status=status,
                    insert_time=payment_date,
                    order=order,
                    tg_user=user,
                    fiat_amount=fiat_amount,
                    currency=currency
                )

    return HttpResponse(200)

