import os
import qrcode
from dotenv import load_dotenv
from telegram.ext.updater import Updater
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import GiftOrder, Payment, TgUser, PaymentStatus, CurrencyDetail
from .utils import get_fiat_amount
from .config import payment_conf, admin_payment_conf, profile_msg

load_dotenv()

TG_TOKEN = os.getenv('TELEGRAM_TOKEN', None)
updater = Updater(TG_TOKEN, use_context=True)


def notify_user(payment, order):
    fiat_amount = get_fiat_amount(
        payment.currency, order.offer.buy_cur, payment.amount
    )
    payment.fiat_amount = round(fiat_amount, 2)
    
    if order.price - 1 <= fiat_amount:
        status = 'success'
    else:
        status = 'fail'
    
    tg_user = TgUser.objects.get(id=order.user.id)
    admins = list(TgUser.objects.filter(is_admin=True).values_list('chat_id', flat=True))
    
    if tg_user.chat_id:
        updater.bot.sendMessage(
            chat_id=tg_user.chat_id, 
            text=payment_conf[status][tg_user.language_code] % (
                order.__str__(), payment.amount, payment.currency,
                order.offer.buy_cur, fiat_amount, 
            ),
            parse_mode='HTML'
        )
    for chat in admins:
        updater.bot.sendMessage(
            chat_id=chat, 
            text=admin_payment_conf['payment_complete'] % (
                order.__str__(), order.id, 
                payment.amount, payment.currency,
                order.offer.buy_cur, fiat_amount,
                status
            ),
            parse_mode='HTML'
        )

def order_complete(instance):
    LANG = instance.user.language_code
    status = instance.status.name if LANG == 'en' \
        else instance.status.ru_name
    faq = ''
    qr_code = qrcode.make(instance.gift_code)
    qr_code.save(f'static/data/img/{instance.gift_code}')
    
    updater.bot.sendPhoto(
        chat_id=instance.user.chat_id, 
        photo=open(f'static/data/img/{instance.gift_code}', 'rb')
    )
    
    faq = instance.offer.subcategory.faq
    if faq:
        faq = profile_msg['faq'][LANG][3::] % faq
    else:
        faq = ' '
    updater.bot.sendMessage(
        chat_id=instance.user.chat_id,
        text=profile_msg['complete'][LANG] % (
            instance.__str__(), instance.gift_code,
            status, instance.amount, faq
        ),
        parse_mode='HTML'
    )


@receiver(pre_save, sender=GiftOrder)
def on_change_gift_txid(sender, instance: GiftOrder, **kwargs):
    if instance.id:
        previous = GiftOrder.objects.filter(id=instance.id)
        if previous:
            previous = previous[0]
            if previous.TxID != instance.TxID:
                payment = Payment.objects.filter(TxID=instance.TxID)
                if payment:
                    instance.status = PaymentStatus.objects.get(name='Payment Received')
                    notify_user(payment[0], instance)
                    
            if previous.status != instance.status \
                and instance.status.name == 'Completed':
                    order_complete(instance)
                    

@receiver(pre_save, sender=Payment)
def on_change_payment_txid(sender, instance: Payment, **kwargs):
    order = GiftOrder.objects.filter(TxID=instance.TxID)
    if order:
        order.update(status=PaymentStatus.objects.get(name='Payment Received'))
        order = order[0]
        notify_user(instance, order)
        
    admins = list(TgUser.objects.filter(is_admin=True).values_list('chat_id', flat=True))
    for chat in admins:
        updater.bot.sendMessage(
            chat_id=chat, 
            text=admin_payment_conf['payment'] % (
                instance.amount, instance.currency
            ),
            parse_mode='HTML'
        )
    
    