import logging
import os

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from .models import GiftOrder, Payment, PaymentAddress
from .utils import get_fiat_amount

load_dotenv()

logging.basicConfig(filename='/root/gunicorn.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


@csrf_exempt
def home(request):
    if request.method == 'POST':
        URL = os.getenv('PAYPAL_IPN')
        params = {'cmd': '_notify-validate'}
        params.update(request.POST.dict())
        response = requests.post(URL, params=params)
        
        if response.text == 'VERIFIED':
            logger.info(f"IPN TEST {response.text}")
        else:
            logger.error(f"IPN TEST {response.text}")
            
        amount = request.POST.get('mc_gross')
        status = request.POST.get('payment_status', False)
        txn_id = request.POST.get('txn_id')
        currency = request.POST.get('mc_currency')
        receiver_email = request.POST.get('receiver_email')
        payment_date = request.POST.get('payment_date')
        logger.info(request.POST.__dict__)
        logger.info(f'\n\n {status}')

        if status == 'Completed':
            user = None
            fiat_amount = None
            order = GiftOrder.objects.filter(
                TxID=txn_id
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
                TxID=txn_id,
                amount=amount,
                address=address[0],
                status=status,
                insert_time=payment_date,
                order=order,
                tg_user=user,
                fiat_amount=fiat_amount,
                currency=currency
            )
            payment.save()

    return HttpResponse(200)

