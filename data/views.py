
import os
import json
from dotenv import load_dotenv
from telegram.ext.updater import Updater

from django.http import HttpResponse
from django.shortcuts import render
from .models import TgUser, CurrencyDetail
from django.views.decorators.csrf import csrf_exempt
load_dotenv()


# @csrf_exempt
# def home1(request):
#     print(request.payment_status)

#     return HttpResponse(200)

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver

@csrf_exempt
@receiver(valid_ipn_received)
def home(sender, **kwargs):
    print(kwargs)
    ipn_obj = sender
    if ipn_obj.payment_status == "Completed":
           print(ipn_obj)