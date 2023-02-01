import sys
import os
import logging
import requests
from dotenv import load_dotenv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, PaymentAddress, GiftOrder
from .utils import get_fiat_amount

sys.stdout = open('/root/gunicorn.log', 'a')
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
        logger.info(request.POST.get('mc_gross'))
        response = requests.post(URL, params=params)
        logger.info(f"IPN TEST {response.text}, {request.POST.get('mc_gross')}")
        if response.text == 'VERIFIED':
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

