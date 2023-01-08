import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'paxfull_gifts.settings'
django.setup()

from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup, InputMediaPhoto, Re
)
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from config import TG_TOKEN
import requests

updater = Updater(TG_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    buttons = [
        [KeyboardButton('Gifts')],
        [KeyboardButton('Help'), KeyboardButton('Contact')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Welcome to my bot',
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def help(update: Update, context: CallbackContext):
    update.message.reply_text("This is Help center")

def contact(update: Update, context: CallbackContext):
    update.message.reply_text("Wait for the support team response")

def gifts(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton('Gift 1')],
        [InlineKeyboardButton('Gift 2')],
        [InlineKeyboardButton('Gift 3')],
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Choose Gift',
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def messageHandler(update: Update, context: CallbackContext):
    if 'Help' in update.message.text:
        help(update, context)
    if 'Contact' in update.message.text:
        contact(update, context)
    if 'Gifts' in update.message.text:
        gifts(update, context)

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('contact', contact))
updater.dispatcher.add_handler(CommandHandler('gifts', gifts))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))




updater.start_polling()