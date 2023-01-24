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


def notify_user(payment, order):
    fiat_amount = payment.fiat_amount
    if not fiat_amount:
        fiat_amount = get_fiat_amount(
            order.offer.buy_cur, payment.currency, payment.amount
        )
        payment.fiat_amount = fiat_amount
        payment.save()
    if order.price - 1 >= fiat_amount:
        status = 'success'
    else:
        status = 'fail'
    
    tg_user = TgUser.objects.get(id=order.user.id)
    admins = list(TgUser.objects.filter(is_admin=True).values_list('chat_id', flat=True))
    
    updater.bot.sendMessage(
        chat_id=chat, 
        text=payment_conf[status][tg_user.language_code] % (
            order.__str__(), order.id, 
            payment.amount, payment.currency,
            order.offer.buy_cur, fiat_amount,
            status
        )
    )
    for chat in admins:
        updater.bot.sendMessage(
            chat_id=chat, 
            text=admin_payment_conf['payment_complete'] % (
                order.__str__(), payment.amount, payment.currency,
                order.offer.buy_cur, fiat_amount, 
            )
        )


@receiver(pre_save, sender=GiftOrder)
def on_change(sender, instance: GiftOrder, **kwargs):
    if instance.id:
        previous = GiftOrder.objects.get(id=instance.id)
        if previous.TxID != instance.TxID:
            payment = Payment.objects.filter(TxID=instance.TxID)
            if payment:
                notify_user(payment, instance)
                    

@receiver(pre_save, sender=Payment)
def on_change(sender, instance: Payment, **kwargs):
    if instance.id:
        order = GiftOrder.objects.filter(TxID=instance.TxID)
        if order:
            notify_user(instance, order)
        else:
            admins = list(TgUser.objects.filter(is_admin=True).values_list('chat_id', flat=True))
            for chat in admins:
                updater.bot.sendMessage(
                    chat_id=chat, 
                    text=admin_payment_conf['payment_complete'] % (
                        instance.amount, instance.currency
                    )
                )
    
    