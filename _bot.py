import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'paxfull_gifts.settings'
django.setup()

import json
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup
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
    category_msg, subcategory_msg, offer_msg,
    operations
)
from data.models import Category, Subcategory, Offer, TgUser

updater = Updater(TG_TOKEN, use_context=True)
dispatcher = updater.dispatcher
LANG = 'en'


def start(update: Update, context: CallbackContext):
    values = {
        'username': update.message.from_user.username,
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


def description(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    buttons = [
        [KeyboardButton(btns['gifts'][LANG])],
        [
            KeyboardButton(btns['profile'][LANG]),
            KeyboardButton(btns['help'][LANG]),
            KeyboardButton(btns['contact'][LANG])
        ],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=description_txt[LANG],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def help(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    update.message.reply_text("This is Help center")

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
    LANG = update.message.from_user.language_code

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
    LANG = user.language_code
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
        if cur and cur != currency_msg['null']:
            user.currency = cur
            user.save()
    offers = Offer.objects.filter(margin__gte=15).select_related('category')
    if user.currency:
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
    if user.currency:
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


def offers(update: Update, context: CallbackContext, user=None):
    if not user:
        user = TgUser.objects.get(tg_id=update.message.from_user.id)
    LANG = user.language_code
    offers = Offer.objects.filter(
        margin__gte=15,
        subcategory__id=eval(update.callback_query.data)['id']
    )
    if user.currency:
        offers = offers.filter(buy_cur=user.currency)
    if offers:
        subcategory_name = offers[0].subcategory.name if LANG == 'en' else offers[0].subcategory.ru_name
        keyboard = list()
        for offer in offers:
            callback_data = {
                'n': 0,
                'id': offer.id,
                'b': False,
                't': 2
            }
            if len(str(callback_data).encode('utf-8')) < 65:
                keyboard.append(
                    [InlineKeyboardButton(offer.display_name(), callback_data=str(callback_data))]
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

    # RU
    'Помощь': help,
    'Контакт': contact,
    'Профиль': profile,
    'Гифты': gifts,
}


def optionsHandler(update: Update, context: CallbackContext):
    user = TgUser.objects.get(tg_id=update.callback_query.message.chat.id)
    data = eval(update.callback_query.data)
    if data['b']:
        msg_handler[operations[data['t']]](update, context, user)
    else:
        msg_handler[operations[data['n']]](update, context, user)


def messageHandler(update: Update, context: CallbackContext):
    user = TgUser.objects.get(tg_id=update.message.from_user.id)
    if type(msg_handler[update.message.text]) == dict:
        for foo in msg_handler[update.message.text]['before']:
            foo['func'](*foo['args'], update, user)
        msg_handler[update.message.text]['after'](update, context, user)
    else:
        msg_handler[update.message.text](update, context, user)


def unknown_text(update: Update, context: CallbackContext):
    LANG = update.message.from_user.language_code
    update.message.reply_text(
        "Sorry I can't recognize your message: '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    LANG = update.message.from_user.language_code
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


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
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))




updater.start_polling()

