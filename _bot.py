import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'paxfull_gifts.settings'
django.setup()

import qrcode
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, 
    KeyboardButton, ReplyKeyboardMarkup
)
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext import CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from config import TG_TOKEN
from bot_txt_conf import (
    currency_msg, lang_txt, description_txt, btns,
    category_msg, subcategory_msg, offer_msg, amount_msg,
    payment_msg, emoji, unknown_msg, help_msg, order_msg, 
    operations
)
from data.models import (
    Category, Subcategory, Offer, 
    TgUser, GiftOrder, PaymentAddress,
    PaymentMethod
)

updater = Updater(TG_TOKEN, use_context=True)
dispatcher = updater.dispatcher
LANG = 'en'


def start(update: Update, context: CallbackContext, *args):
    username = getattr(update.message.from_user, 'username', 'unknown')
    values = {
        'username': username,
        'first_name': update.message.from_user.first_name,
        'native_language_code': update.message.from_user.language_code,
        'is_bot': update.message.from_user.is_bot
    }
    user, created = TgUser.objects.update_or_create(
        tg_id=update.message.from_user.id, defaults=values
    )
    user.currency = None
    user.save()
    buttons = [
        [KeyboardButton('-- EN --'), KeyboardButton('-- RU --')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=lang_txt.get(user.native_language_code, user.language_code),
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def description(update: Update, context: CallbackContext, user=None, msg=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    buttons = [
        [KeyboardButton(btns['gifts'][LANG])],
        [
            KeyboardButton(emoji['en' if LANG == 'ru' else 'ru']),
            KeyboardButton(btns['profile'][LANG]),
            KeyboardButton(btns['help'][LANG]),
        ],
    ]
    if user.currency:
        buttons[1].append(KeyboardButton(user.currency))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=description_txt[LANG] if not msg else msg,
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def help(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    update.message.reply_text(help_msg[LANG])

def contact(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    update.message.reply_text("Wait for the support team response")

def profile(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = update.message.from_user.language_code
    update.message.reply_text("Your profile")


def currency(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code

    offers = Offer.objects.filter(margin__gte=15)
    currencies = list(set(offers.values_list('buy_cur', flat=True)))
    keyboard = list()
    callback_data = {
        'n': 1,
        'cur': '',
        'b': False
    }
    for cur in currencies:
        callback_data['cur'] = cur
        keyboard.append([InlineKeyboardButton(cur, callback_data=str(callback_data))])
    callback_data['cur'] = currency_msg['null']
    keyboard.append([InlineKeyboardButton(currency_msg['all'][LANG], callback_data=str(callback_data))])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=currency_msg['txt'].get(LANG, 'en'),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def gifts(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    if not user.currency:
        currency(update, context, user)
    else:
        category(update, context, user)


def category(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code

    callback_data = update.__getitem__('callback_query')
    if callback_data:
        data = eval(update.callback_query.data)
        cur = data.get('cur', None)
        if cur:
            user.currency = cur
            user.save()
            description(update, context, user, currency_msg['msg'][LANG] %cur)
    offers = Offer.objects.filter(margin__gte=15).select_related('category')
    if user.currency !=  'ALL':
        offers = offers.filter(buy_cur=user.currency)
    if offers:
        categories = set(offers.values_list('category__id', flat=True))
        category_objs = Category.objects.filter(id__in=categories)
        keyboard = list()
        for category in category_objs:
            category_name = category.name if LANG == 'en' else category.ru_name
            callback_data = {
                'n': 2,
                'id': category.id,
                'b': False
            }
            keyboard.append([InlineKeyboardButton(category_name, callback_data=str(callback_data))])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=category_msg.get(LANG, 'en'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No Gifts",
        )

def subcategory(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    data = eval(update.callback_query.data)
    if data['b']:
        data['id'] = Offer.objects.get(id=data['id']).category.id
    offers = Offer.objects.filter(
        margin__gte=15,
        category__id=data['id']
    ).select_related('subcategory')
    if user.currency != 'ALL':
        offers = offers.filter(buy_cur=user.currency)
    if offers:
        sub_cat_ids = set(offers.values_list('subcategory__id', flat=True))
        sub_category_objs = Subcategory.objects.filter(id__in=sub_cat_ids)
        category_name = sub_category_objs[0].category.name if LANG == 'en' else sub_category_objs[0].category.ru_name
        keyboard = list()
        for sub_category in sub_category_objs:
            sub_category_name = sub_category.name if LANG == 'en' else sub_category.ru_name
            callback_data = {
                'n': 0,
                'id': sub_category.id,
                'b': False,
                't': 1
            }
            keyboard.append(
                [InlineKeyboardButton(sub_category_name, callback_data=str(callback_data))]
            )
    callback_data['b'] = True
    keyboard.append([
        InlineKeyboardButton(
            subcategory_msg['back'].get(LANG, 'en'),
            callback_data=str(callback_data)
        )
    ])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='. '.join([
            category_name,
            subcategory_msg['msg'].get(LANG, 'en')
        ]),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def get_display_offers(offers: Offer):
    display_offers = [offers[0]]
    min = offers[0].offer_detail.fiat_amount_range_min
    max = offers[0].offer_detail.fiat_amount_range_max
    pr_amount = offers[0].offer_detail.predefined_amount \
        if type(offers[0].offer_detail.predefined_amount) == list else []
    for idx in range(1, len(offers)):
        if offers[idx].offer_info() != offers[idx-1].offer_info():
            if offers[idx].offer_detail.predefined_amount != 'null':
                if set(offers[idx].offer_detail.predefined_amount) - set(pr_amount):
                    pr_amount.extend(offers[idx].offer_detail.predefined_amount)
                    display_offers.append(offers[idx])
            elif offers[idx].offer_detail.fiat_amount_range_min < min:
                min = offers[idx].offer_detail.fiat_amount_range_min
                display_offers.append(offers[idx])
            elif offers[idx].offer_detail.fiat_amount_range_max > max:
                max = offers[idx].offer_detail.fiat_amount_range_max
                display_offers.append(offers[idx])
    return display_offers


def offers(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    offers = Offer.objects.filter(
        margin__gte=15,
        subcategory__id=eval(update.callback_query.data)['id']
    ).order_by('-margin').select_related('offer_detail')
    if user.currency != 'ALL':
        offers = offers.filter(buy_cur=user.currency)
    if offers:
        subcategory_name = offers[0].subcategory.name if LANG == 'en' else offers[0].subcategory.ru_name
        keyboard = list()
        callback_data = {
            'n': 3,
            'id': '',
            'b': False,
            't': 2
        }
        display_offers = get_display_offers(offers)
        for offer in display_offers:
            callback_data['id'] = offer.id
            if len(str(callback_data).encode('utf-8')) < 65:
                keyboard.append(
                    [InlineKeyboardButton(offer.__str__(), callback_data=str(callback_data))]
                )
            else:
                print(f"Can't parse inline keyboard button: b{len(str(callback_data).encode('utf-8'))}")
        callback_data['b'] = True
        keyboard.append([
            InlineKeyboardButton(
                offer_msg['back'].get(LANG, 'en'),
                callback_data=str(callback_data)
            )
        ])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='. '.join([
                subcategory_name,
                offer_msg['msg'].get(LANG, 'en')
            ]),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


def offer_desc(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    offer = Offer.objects.get(id=eval(update.callback_query.data)['id'])
    callback_data = {
        'n': 5,
        'id': offer.id,
        'b': False,
        't': 3
    }
    back = callback_data.copy()
    back.update({'b': True, 't': 0, 'id': offer.subcategory.id})
    continue_ = callback_data.copy()
    continue_.update({'n': 6})
    keyboard = [
        [InlineKeyboardButton(btns['terms_of_use'][LANG], callback_data=str(callback_data))],
        [
            InlineKeyboardButton(btns['back'][LANG], callback_data=str(back)),
            InlineKeyboardButton(btns['continue'][LANG], callback_data=str(continue_))
        ]
    ]
    
    warranty = offer_msg['warranty']['msg'][LANG]
    if offer.warranty:
        warranty = offer.warranty.split(' ')
        if offer_msg['warranty']['time'].get(warranty[1], None):
            warranty = warranty[0] + " " + offer_msg['warranty']['time'][warranty[1]][LANG]
    
    country = offer.currency.country if offer.currency.country \
                else offer_msg['country'][LANG] % offer.currency.code
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=offer_msg['desc'][LANG] % (
            offer.__str__(), 
            warranty, 
            country,
            offer.display_amount(), 
            offer_msg['faq'][LANG] % offer.subcategory.faq if offer.subcategory.faq else '' 
        ),
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode='HTML'
    )

def amount(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    offer = Offer.objects.get(id=eval(update.callback_query.data)['id'])
    
    # create Order instance
    GiftOrder.objects.update_or_create(
        status='Open',
        offer=offer,
        discount=offer.get_discount(),
        user=user
    )
    
    callback_data = {
        'n': 4,
        'id': offer.id,
        'a': 0,
        'b': False,
        't': 0
    }
    back = callback_data.copy()
    back.update({'id': offer.subcategory.id, 'b': True})
    keyboard = list()
    
    if offer.offer_detail.predefined_amount != 'null':   
        for amount in offer.offer_detail.predefined_amount:
            callback_data['a'] = amount
            keyboard.append(
                [
                    InlineKeyboardButton(str(amount) + ' ' + offer.buy_cur, 
                    callback_data=str(callback_data))
                ]
            )
        keyboard.append([
            InlineKeyboardButton(btns['back'][LANG], 
            callback_data=str(back))
        ])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=amount_msg['choose_amount'][LANG],
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
            
        )
    else:
        keyboard = [[
            InlineKeyboardButton(btns['back'][LANG], 
            callback_data=str(back))
        ]]
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=amount_msg['enter_amount'][LANG] % (offer.display_amount(), offer.id),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        

def payments_method(update: Update, context: CallbackContext, user=None, order: GiftOrder=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    
    if not order:
        data = eval(update.callback_query.data)
        offer = Offer.objects.get(id=data['id'])
        order, created = GiftOrder.objects.update_or_create(
            status='Open',
            offer=offer,
            discount=offer.get_discount(),
            user=user, 
            defaults={'amount': data['a']}
        )
        
    methods = PaymentMethod.objects.filter(is_active=True)
    callback_data = {
        'n': 7,
        'id': order.callback_id,
    }
    keyboard = list()
    for method in methods:
        callback_data.update({'t': method.id})
        print(callback_data)
        keyboard.append([
            InlineKeyboardButton(str(method), callback_data=str(callback_data))
        ])
        
    callback_data.update({'b': True, 't': 0, 'id': order.offer.subcategory.id})
    print(callback_data)
    keyboard.append([
        InlineKeyboardButton(btns['back'][LANG], 
        callback_data=str(callback_data))
    ])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=payment_msg['method'][LANG] % (
            order.offer.__str__(), str(order.amount),
            str(order.get_price()), order.offer.buy_cur
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
            

def payment_address(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    
    addresses = PaymentAddress.objects.filter(
        is_active=True,
        method__id=eval(update.callback_query.data)['t']
    )
    order = GiftOrder.objects.get(callback_id=eval(update.callback_query.data)['id'])
    callback_data = {
        'n': 8,
        'id': order.callback_id,
    }
    keyboard = list()
    if len(addresses) > 1:
        for address in addresses:
            callback_data.update({'t': address.id})
            keyboard.append([
                InlineKeyboardButton(str(address), callback_data=str(callback_data))
            ])
        
        callback_data.update({'b': True, 't': 0, 'id': order.offer.subcategory.id})
        keyboard.append([
            InlineKeyboardButton(btns['back'][LANG], 
            callback_data=str(callback_data))
        ])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=payment_msg['address'][LANG],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        complete_payment(
            update, context, user,
            {
                'order': order,
                'address': addresses[0]
            }
        )
        
        
def complete_payment(
    update: Update, context: CallbackContext, 
    user=None, data:dict=None
):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    
    if data:
        order = data['order']
        address = data['address']
    else:
        order = GiftOrder.objects.get(callback_id=eval(update.callback_query.data)['id'])
        address = PaymentAddress.objects.get(id=eval(update.callback_query.data)['t'])

    order.status = 'Pending'
    order.price = order.get_price()
    order.save()
    qr_code = qrcode.make(address.address)
    qr_code.save(f'static/data/img/{address.address}')
    context.bot.send_photo(
        chat_id=update.effective_chat.id, 
        photo=open(f'static/data/img/{address.address}', 'rb')
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=payment_msg['complete'][LANG] % (
            address.address, order.id, 
            order.offer.__str__(), str(order.amount),
            str(order.price), order.offer.buy_cur
        ),
        parse_mode = 'HTML'
    )
    
    

def terms_of_use(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    offer = Offer.objects.get(id=eval(update.callback_query.data)['id'])
    callback_back = {
        'n': 6,
        'id': offer.id,
        'b': True,
        't': 3
    }
    callback_continue = callback_back.copy()
    callback_continue['b'] = False
    keyboard = [
        [
            InlineKeyboardButton(btns['back'][LANG], callback_data=str(callback_back)),
            InlineKeyboardButton(
                btns['continue'][LANG], 
                callback_data=str(callback_continue)
            )
        ]
    ]
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=offer_msg['terms_of_use'][LANG],
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode='HTML'
    )
    

def update_lang(lang:str, update: Update, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    user.language_code = lang
    user.save()
    global LANG
    LANG = lang


msg_handler = {
    '-- EN --': {
        'before': [
            {
                'func': update_lang,
                'args': ['en']
            }
        ],
        'after': description
    },
    '-- RU --': {
        'before': [
            {
                'func': update_lang,
                'args': ['ru']
            }
        ],
        'after': description
    },
    'Help': help,
    'Contact': contact,
    'Profile': profile,
    'Gifts': gifts,
    'gifts': gifts,
    'category': category,
    'subcategory': subcategory,
    'offers': offers,
    'currency': currency,
    'offer_desc': offer_desc,
    'payment_method': payments_method,
    'terms_of_use': terms_of_use,
    'amount': amount,
    'address': payment_address,
    'complete': complete_payment,

    # RU
    'Помощь': help,
    'Контакт': contact,
    'Профиль': profile,
    'Гифты': gifts,

    # emoji
    '\U0001F1EC\U0001F1E7': {
        'before': [
            {
                'func': update_lang,
                'args': ['en']
            }
        ],
        'after': description
    },
    '\U0001F1F7\U0001F1FA': {
        'before': [
            {
                'func': update_lang,
                'args': ['ru']
            }
        ],
        'after': description
    },
}


def optionsHandler(update: Update, context: CallbackContext):
    user = TgUser.objects.get(tg_id=update.callback_query.message.chat.id)
    data = eval(update.callback_query.data)
    if data.get('b', None):
        msg_handler[operations[data['t']]](update, context, user)
    else:
        msg_handler[operations[data['n']]](update, context, user)


def messageHandler(update: Update, context: CallbackContext):
    user = TgUser.objects.get(tg_id=update.message.from_user.id)
    if msg_handler.get(update.message.text, None):
        if type(msg_handler[update.message.text]) == dict:
            for foo in msg_handler[update.message.text]['before']:
                foo['func'](*foo['args'], update, user)
            msg_handler[update.message.text]['after'](update, context, user)
        else:
            msg_handler[update.message.text](update, context, user)
    elif len(update.message.text.split(':')) == 2:
        order = update.message.text.split(':')
        if order[0].isdigit() and order[1].isdigit():
            offer = Offer.objects.filter(id=order[0]).first()
            if offer:
                user_order = GiftOrder.objects.filter(
                    user=user,
                    offer=offer,
                    status='Open'
                ).order_by('-created_at').first()
                if user_order:
                    if int(order[1]) >= offer.offer_detail.fiat_amount_range_min and\
                        int(order[1]) <= offer.offer_detail.fiat_amount_range_max:
                        user_order.amount = int(order[1])
                        user_order.save()
                        payments_method(update, context, user, user_order)
                    else:
                        # Invalid input amount
                        unknown(
                            update, context, user, 
                            order_msg['invalid_amount'][LANG] % (
                                offer.display_amount(), offer.id
                            )
                        )
                else:
                    # No active order found
                    unknown(update, context, user, order_msg['no_active_orders'][LANG])
            else:
                # Offer by this ID not found
                unknown(update, context, user, order_msg['offer_not_found'][LANG])
    else:
        offers = Offer.objects.all()
        currencies = list(offers.values_list('buy_cur', flat=True))
        currencies.append('ALL')
        if update.message.text in set(currencies):
            currency(update, context, user)
        else:
            unknown(update, context, user)
            

def unknown(update: Update, context: CallbackContext, user=None, msg=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    buttons = [
        [KeyboardButton(btns['gifts'][LANG])],
        [
            KeyboardButton(emoji['en' if LANG == 'ru' else 'ru']),
            KeyboardButton(btns['profile'][LANG]),
            KeyboardButton(btns['help'][LANG]),
        ],
    ]
    if user.currency:
        buttons[1].append(KeyboardButton(user.currency))
    text = unknown_msg[LANG] % update.message.text
    if msg:
        text = msg
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
        parse_mode='HTML'
    )


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('description', description))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('contact', contact))
updater.dispatcher.add_handler(CommandHandler('profile', profile))
updater.dispatcher.add_handler(CommandHandler('gifts', gifts))
updater.dispatcher.add_handler(CommandHandler('currency', currency))

updater.dispatcher.add_handler(CallbackQueryHandler(optionsHandler))

updater.dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))


updater.start_polling()

