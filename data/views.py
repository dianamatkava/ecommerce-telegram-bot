import os
import requests
from dotenv import load_dotenv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

load_dotenv()


@csrf_exempt
def home(request):
    if request.method == 'POST':
        URL = os.getenv('PAYPAL_IPN', 'TEST_PAYPAL_IPN')
        params = {'cmd': '_notify-validate'}
        params.update(request.POST.dict())
        response = requests.post(URL, params=params)
        print(response.text)
        print(request.POST.__dict__)

        if response.text == 'VERIFIED':
            transaction_id = request.POST.get('txn_id')
            payment_status = request.POST.get('payment_status')
            amount = request.POST.get('mc_gross')
            print(request.POST.__dict__)

            return HttpResponse("IPN message verified")
        else:
            return HttpResponse("IPN message not verified")
    else:
        return HttpResponse("Invalid request method")