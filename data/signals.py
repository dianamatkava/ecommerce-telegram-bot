import os
from dotenv import load_dotenv
from telegram.ext.updater import Updater
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import GiftOrder, Payment, TgUser
from .utils import get_fiat_amount
from config import payment_conf, admin_payment_conf

load_dotenv()

TG_TOKEN = os.getenv('TELEGRAM_TOKEN', None)
updater = Updater(TG_TOKEN, use_context=True)

@receiver(pre_save, sender=GiftOrder)
def on_change(sender, instance: GiftOrder, **kwargs):
    if instance.id:
        previous = GiftOrder.objects.get(id=instance.id)
        if previous.TxID != instance.TxID:
            payment = Payment.objects.filter(TxID=instance.TxID)
            if payment:
                fiat_amount = payment.fiat_amount
                if not fiat_amount:
                    fiat_amount = get_fiat_amount(
                        instance.offer.buy_cur, payment.currency, payment.amount
                    )
                    payment.fiat_amount = fiat_amount
                    payment.save()
                if instance.price - 1 >= fiat_amount:
                    status = 'success'
                else:
                    status = 'fail'
                
                tg_user = TgUser.objects.get(id=instance.user.id)
                admins = list(TgUser.objects.filter(is_admin=True).values_list('chat_id', flat=True))
                
                updater.bot.sendMessage(
                    chat_id=chat, 
                    text=admin_payment_conf['payment'] % (
                        instance.__str__(), instance.id, 
                        payment.amount, payment.currency,
                        instance.offer.buy_cur, fiat_amount,
                        status
                    )
                )
                for chat in admins:
                    updater.bot.sendMessage(
                        chat_id=chat, 
                        text=payment_conf[status][tg_user.language_code] % (
                            instance.__str__(), payment.amount, payment.currency,
                            instance.offer.buy_cur, fiat_amount, 
                        )
                    )
                    
                    