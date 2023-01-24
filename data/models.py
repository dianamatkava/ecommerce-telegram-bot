import os
import uuid
import requests
from dotenv import load_dotenv
from .utils import generate_url
from django.db import models

load_dotenv()


class Category(models.Model):
    px_id = models.IntegerField()
    name = models.CharField(max_length=255)
    ru_name = models.CharField(max_length=255)
    px_slug = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return f'{self.name} / {self.ru_name}'


class Tag(models.Model):
    px_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1025)
    px_slug = models.CharField(max_length=255)
    

    def __str__(self) -> str:
        return f'{self.name}'


class Subcategory(models.Model):
    px_id = models.IntegerField()
    name = models.CharField(max_length=255)
    ru_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'Category',
        db_column = 'category_id',
        on_delete=models.PROTECT
    )
    faq = models.CharField(max_length=1000, blank=True, null=True)
    px_slug = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "subcategories"
        
    def __str__(self) -> str:
        return f'{self.name} / {self.ru_name}'


class Offer(models.Model):
    PX_SELL = 'sell'
    PX_BUY = 'buy'
    OFFER_TYPE = [
        (PX_SELL, 'Sell'),
        (PX_BUY, 'Buy')
    ]
    BTC = 'BTC'
    USDT = 'USDT'
    CURRENCIES = [
        (BTC, 'Bitcoin'),
        (USDT, 'Tether')
    ]

    px_id = models.CharField(max_length=255)
    sell_cur = models.CharField(
        'cryptoCurrencyCode', max_length=128, choices=CURRENCIES
    )
    buy_cur = models.CharField('fiatCurrencyCode', max_length=128)
    currency = models.ForeignKey(
        'CurrencyDetail',
        db_column = 'currency_ditail_id',
        on_delete=models.PROTECT,
        null=True
    )
    margin = models.FloatField()
    price_per_cur = models.FloatField('pricePerUsd')
    require_verified_id = models.BooleanField()
    tags = models.ManyToManyField('Tag', related_name='offers', blank=True)
    category = models.ForeignKey(
        'Category',
        db_column = 'category_id',
        on_delete=models.PROTECT,
    )
    subcategory = models.ForeignKey(
        'Subcategory',
        db_column = 'subcategory_id',
        on_delete=models.PROTECT
    )
    payment_method_label = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    warranty = models.CharField(max_length=255, null=True, blank=True)
    username =  models.CharField(max_length=255)
    score = models.FloatField()
    last_seen = models.CharField('lastSeenString', max_length=255)
    average_trade_speed = models.CharField("releaseTimeMedianHumanize", max_length=255)
    user_timezone = models.CharField(max_length=255)
    offer_type = models.CharField(
        max_length=128, choices=OFFER_TYPE, default=PX_SELL
    )
    offer_detail = models.OneToOneField(
        'OfferDetail',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def offer_info(self):
        margin = self.margin
        predefined_amount = self.offer_detail.predefined_amount
        min = self.offer_detail.fiat_amount_range_min
        max = self.offer_detail.fiat_amount_range_max
        return f'{margin} - {predefined_amount} - {min} - {max}'
    
    def display_amount(self):
        predefined_amount = self.offer_detail.predefined_amount
        min = self.offer_detail.fiat_amount_range_min
        max = self.offer_detail.fiat_amount_range_max
        res = str()
        if predefined_amount != 'null':
            if len(predefined_amount) > 1:
                res += f" {', '.join(str(x) for x in predefined_amount)} {self.buy_cur}."
            else:
                res += f" {predefined_amount[0]} {self.buy_cur}"
        else:
            if min != 'null':
                res += f' min: {min}'
            if max != 'null':
                res += f' | max: {max} {self.buy_cur}.'
        return f'{res}'

    def get_discount(self):
        return round((self.margin-5)/2)

    def __str__(self) -> str:
        name = self.subcategory.name
        margin = self.get_discount()
        res = f'{name}' if len(name) <= 20 else f"{name.replace('Gift Cart', '')}"
        res += self.display_amount()
        return f'-{margin}% {res}'


class OfferDetail(models.Model):
    px_id = models.CharField(max_length=255)
    feedback_negative = models.IntegerField()
    feedback_positive = models.IntegerField()
    predefined_amount = models.JSONField(blank=True)
    fiat_amount_range_min = models.IntegerField()
    fiat_amount_range_max = models.IntegerField()
    fiat_price_per_btc = models.FloatField()
    price_per_btc = models.FloatField()
    fee_percentage = models.IntegerField()
    payment_method_group_id = models.IntegerField()
    percent_per_usd = models.FloatField()
    require_full_name_visibility = models.BooleanField()
    default_flow_type = models.CharField(max_length=255)


class TgUser(models.Model):
    tg_id = models.IntegerField()
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    native_language_code = models.CharField(max_length=2)
    language_code = models.CharField(max_length=2, null=True)
    currency = models.CharField(max_length=3, null=True)
    is_bot = models.BooleanField()
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username


class GiftOrder(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    callback_id = models.AutoField(primary_key=True)
    status = models.ForeignKey(
        'PaymentStatus',
        db_column='payment_status_id',
        on_delete=models.SET_NULL,
        null=True
    )
    offer = models.ForeignKey(
        'Offer', 
        db_column='offer_id',
        on_delete=models.SET_NULL,
        null=True
    )
    discount = models.FloatField()
    amount = models.IntegerField(default=0)
    price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        'TgUser', 
        db_column='tg_user_id',
        on_delete=models.CASCADE
    )
    TxID = models.CharField(max_length=255, null=True, blank=True)
    payment_address = models.ForeignKey(
        'PaymentAddress', 
        db_column='payment_address_id',
        on_delete=models.SET_NULL,
        null=True
    )
    
    def get_price(self):
        return self.amount - (self.amount * self.discount / 100)
    
    def to_crypto(self, coin):
        URL = os.getenv('COINGATE_RATE_API', None)
        headers = {"accept": "text/plain"}
        response = requests.get(
            generate_url([URL, self.offer.currency.code, coin]), 
            headers=headers
        )
        if response.status_code == 200:
            return round(float(response.text) * self.get_price(), 8)
        else:
            return response.status_code
    
    def __str__(self):
        res = ''
        if self.payment_address:
            res += self.payment_address.name
        res += f" {int(self.discount)}% {self.offer.subcategory.name} {self.amount} {self.offer.buy_cur}"
        return res


class CurrencyDetail(models.Model):
    CRYPTO = 'crypto'
    FIAT = 'fiat'
    TYPE = [
        (CRYPTO, 'Crypto'),
        (FIAT, 'Fiat')
    ]
    code = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPE, default=FIAT)
    
    def __str__(self):
        return f'{self.code} {self.country}'
    
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    api_key_conf = models.CharField(max_length=128, blank=True, null=True)
    secret_key_conf = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.display_name


class PaymentAddress(models.Model):
    name = models.CharField(max_length=510)
    address = models.CharField(max_length=255)
    network = models.CharField(
        max_length=255, blank=True, null=True
    )
    method = models.ForeignKey(
        'PaymentMethod',
        db_column='payment_method_id',
        on_delete=models.SET_NULL,
        null=True
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        res = self.name
        if self.network:
            res += f" Network: {self.network}"
        return res
    
    
class Payment(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    TYPE = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw')
    ]
    bc_id = models.CharField(max_length=255, null=True)
    TxID = models.CharField(max_length=255, null=True)
    amount = models.PositiveIntegerField()
    address = models.ForeignKey(
        'PaymentAddress',
        db_column='payment_address_id',
        on_delete=models.SET_NULL,
        null=True
    )
    _type = models.CharField(max_length=255, choices=TYPE, default=DEPOSIT)
    status = models.BooleanField(default=True, null=True)
    insert_time = models.CharField(max_length=255)
    order = models.ForeignKey(
        'GiftOrder',
        db_column='payment_id',
        on_delete=models.SET_NULL,
        null=True
    )
    tg_user = models.ForeignKey(
        'TgUser',
        db_column='tg_user_id',
        on_delete=models.SET_NULL,
        null=True
    )
    
    
class PaymentStatus(models.Model):
    name = models.CharField(max_length=128, unique=True)
    ru_name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "payment statuses"
    
    def __str__(self):
        return self.name
    