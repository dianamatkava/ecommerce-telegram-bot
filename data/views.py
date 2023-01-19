
import os
from dotenv import load_dotenv
from telegram.ext.updater import Updater

from django.http import HttpResponse
from django.shortcuts import render
from .models import TgUser, CurrencyDetail

load_dotenv()

def home(request):
    # user = TgUser.objects.get(id=1)
    # updater = Updater(os.getenv('TELEGRAM_TOKEN', None))
    # updater.bot.sendMessage(chat_id=user.tg_id, text='Hello there!')

    return HttpResponse('')