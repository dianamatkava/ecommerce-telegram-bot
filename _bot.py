import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'paxfull_gifts.settings'
django.setup()

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
from bot_txt_conf import lang, lang_txt, description_txt
from data.models import Category, Subcategory, Offer

updater = Updater(TG_TOKEN, use_context=True)
dispatcher = updater.dispatcher
LANG = ''

def start(update: Update, context: CallbackContext):
    global LANG
    LANG = lang.get(update.message.from_user.language_code, 'en')
    buttons = [
        [KeyboardButton('-- EN --'), KeyboardButton('-- RU --')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=lang_txt[LANG],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def description(update: Update, context: CallbackContext):
    buttons = [
        [KeyboardButton('Gifts')],
        [
            KeyboardButton('Profile'),
            KeyboardButton('Settings'),
            KeyboardButton('Help'),
            KeyboardButton('Contact')
        ],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=description_txt[LANG],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def help(update: Update, context: CallbackContext):
    update.message.reply_text("This is Help center")

def contact(update: Update, context: CallbackContext):
    update.message.reply_text("Wait for the support team response")

# {
#     'update_id': 517899704,
#     'message': {
#         'supergroup_chat_created': False,
#         'new_chat_photo': [],
#         'text': 'Gifts',
#         'channel_chat_created': False,
#         'date': 1673291843,
#         'delete_chat_photo': False,
#         'caption_entities': [],
#         'message_id': 203,
#         'chat': {
#             'id': 357585845,
#             'type': 'private',
#             'username': 'gera_di',
#             'first_name': 'Di'
#         },
#         'group_chat_created': False,
#         'new_chat_members': [],
#         'photo': [],
#         'entities': [],
#         'from': {
#             'is_bot': False,
#             'id': 357585845,
#             'first_name': 'Di',
#             'language_code': 'ru',
#             'username':
#                 'gera_di'
#             }
#         }
#     }


def gifts(update: Update, context: CallbackContext):
    offers = Offer.objects.filter(margin__gte=15).select_related('category')
    categories = set(offers.values_list('category__id', flat=True))
    category_objs = Category.objects.filter(id__in=categories)
    keyboard = list()
    for cat in category_objs:
        keyboard.append([InlineKeyboardButton(cat.name, callback_data=f"{cat.id}")])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Choose Category',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def sub_category(update: Update, context: CallbackContext):
    offers = Offer.objects.filter(
        margin__gte=15,
        category__id=int(update.callback_query.data)
    ).select_related('subcategory')
    sub_cat_ids = set(offers.values_list('subcategory__id', flat=True))
    sub_category_objs = Subcategory.objects.filter(id__in=sub_cat_ids)
    keyboard = list()
    for sub_cat in sub_category_objs:
        keyboard.append([InlineKeyboardButton(sub_cat.name, callback_data=f"{sub_cat.id}")])

    keyboard.append([InlineKeyboardButton('Back to Category', callback_data=f"back")])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Choose Category',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



def update_lang(lang:str):
    # add update user lang info
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
    'Gifts': gifts,
}

def messageHandler(update: Update, context: CallbackContext):
    if type(msg_handler[update.message.text]) == dict:
        for foo in msg_handler[update.message.text]['before']:
            foo['func'](*foo['args'])
        msg_handler[update.message.text]['after'](update, context)
    else:
        msg_handler[update.message.text](update, context)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('description', description))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('contact', contact))
updater.dispatcher.add_handler(CommandHandler('gifts', gifts))

updater.dispatcher.add_handler(CallbackQueryHandler(sub_category))

updater.dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))




updater.start_polling()