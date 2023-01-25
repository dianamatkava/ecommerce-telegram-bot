lang = {
    'en': 'en',
    'ru': 'ru'
}

# Choose lang. Second msg after start
lang_txt = {
    'en': 'Choose Interface Language. You can change language in future in Settings',
    'ru': 'Выберите язык интерфейса. Вы можете изменить язык в будущем в настройках'
}

# !!! Shows desc ab bot. Runs always after lang is chosen. 
description_txt = {
    'en': 'Choose a Gifts from a wide assortment \nfor a good price with discount +10%',
    'ru': 'Выбирайте Гифты из широкого ассортимента \nпо хорошей цене со скидкой +10%'
}

currency_msg = {
    # For btns
    'all': {
        'en': 'See all',
        'ru': 'Посмотреть все'
    },
    'null': 'ALL',
    
    # !!! Before currency has been chosen
    'txt': {
        'en': 'Choose Gifts currency you want to buy or tap on "See all". You can change currency in future in Settings.',
        'ru': 'Выберите валюту подарков, которую хотите купить, или нажмите «Просмотреть все». Вы можете изменить валюту в будущем в настройках.'
    },
    
    # After currency has been chosen
    'msg': {
        'en': 'You chose %s as your currency',
        'ru': 'Вы выбрали %s своей валютой'
    },
}

category_msg = {
    'en': 'Choose Gift category',
    'ru': 'Выберите категорию Гифта'
}

subcategory_msg = {
    'msg': {
        'en': 'Choose Gift subcategory',
        'ru': 'Выберите подкатегорию Гифта'
    },
    'back': {
        'en': 'Back to categories',
        'ru': 'Обратно к категориям'
    },
}

offer_msg = {
    'msg': {
        'en': 'Choose Gift',
        'ru': 'Выберите Гифт'
    },
    'back': {
        'en': 'Back to subcategories',
        'ru': 'Обратно к подкатегориям'
    },
    
    # Offer description
    'desc': {
        'en': """ 
<strong>%s</strong>

- - - - - IMPORTANT INFORMATION - - - - -

1. Warranty period (usage time): <strong>%s</strong>
2. Region restriction: <strong>%s only</strong>
3. Denominations: <strong>%s</strong> 
%s
        """,
        'ru': """
<strong>%s</strong>

- - - - - ВАЖНАЯ ИНФОРМАЦИЯ - - - - -

1. Гарантийный срок (время использования): до <strong>%s</strong>
2. Ограничение по региону: <strong>только %s</strong>
3. Номиналы: <strong>%s</strong>
%s

        """
    },
    'terms_of_use': {
        'en': '''
- - - - - - - - - TERMS OF USE - - - - - - - - -

• We check each card for the correct balance and validity before sending. Sometimes it may take some time. Please wait patiently;

• Before purchasing, you must make sure that the gift cards will work in your country/on your account. We are not responsible for any problems on your side;

• If for any reason you are unable to use received gift cards, we will only be able to cancel the order after we sell them to someone else. In other cases, we have the right not to cancel it;

• You must use your gift cards within the specified warranty period. We cannot guarantee that they will be valid for a longer time if you decide to store them.

• We are looking for reliable partners for honest, long-term and mutually beneficial cooperation. Please contact us if you have any business suggestions/offers.
        ''',
        'ru': '''
        
- - - - - - - - - УСЛОВИЯ ЭКСПЛУАТАЦИИ - - - - - - - - -

• Мы проверяем каждую карту на правильный баланс и действительность перед отправкой. Иногда это может занять некоторое время. Пожалуйста, подождите терпеливо;

• Перед покупкой вы должны убедиться, что подарочные карты будут работать в вашей стране/на вашем аккаунте. Мы не несем ответственности за любые проблемы на вашей стороне;

• Если по какой-либо причине вы не можете использовать полученные подарочные карты, мы сможем отменить заказ только после того, как продадим их кому-то другому. В остальных случаях мы имеем право не отменять его;

• Вы должны использовать подарочные карты в течение указанного гарантийного срока. Мы не можем гарантировать, что они будут действительны в течение более длительного времени, если вы решите их сохранить.

• Мы ищем надежных партнеров для честного, долгосрочного и взаимовыгодного сотрудничества. Пожалуйста, свяжитесь с нами, если у вас есть какие-либо деловые предложения / предложения.
        '''
    },
    'warranty': {
        # !!! If no warranty restriction specified
        'msg': {
            'en': 'Redeem on your account (unlimited after redeeming)',
            'ru': 'Погасить на свой счет (неограниченно после погашения)'
        },
        'time': {
            'days': {
                'en': 'days',
                'ru': 'дней'
            },
            'hours': {
                'en': 'hours',
                'ru': 'часов'
            },
            'hrs': {
                'en': 'hrs',
                'ru': 'часов'
            }
        }
    },
    'faq': {
        'en': '4. Read more (FAQ): %s ',
        'ru': '4. Подробнее (FAQ): %s'
    },
    'country': {
        # !!! If no country restriction specified
        'en': 'Valid in the country whose official currency is %s ',
        'ru': 'Действует в стране официальная валюта которой является %s'
    }
}

amount_msg = {
    'choose_amount': {
        'en': 'Choose Gift amount:',
        'ru': 'Выберите сумму Гифта:'
    },
    'enter_amount': {
        # !!! When Gift amount allows custom input. min: 50 | max: 500
        'en': 'Input your custom amount.\nNote that amount should be between: <strong>\n%s</strong> \nPlease enter Gift ID and amount separated by a colon\nExample: 123:50.\nYour Gift ID: <strong>%s</strong>',
        'ru': 'Введите вашу сумму.\nОбратите внимание, что сумма должна быть между: <strong>\n%s</strong> \nПожалуйста введите ID Гифта и сумму через двоиточие\nПример: 123:50\nID вашего Гифта: <strong>%s</strong>'
    }
}


# Handles user input errors
order_msg = {
    'offer_not_found': {
        'en': 'Gift by this ID not found',
        'ru': 'Нет Гифта по такому ID'
    },
    'no_active_orders': {
        'en': 'No active orders found',
        'ru': 'Активных заказов не найдено'
    },
    'invalid_amount': {
        'en': '<strong>Invalid Gift amount.</strong> \nNote that amount should be between: <strong>\n%s</strong> \nPlease enter Gift ID and amount separated by a colon\nExample: 123:50.\nYour Gift ID: <strong>%s</strong>',
        'ru': '<strong>Неверная сумма Гифта.</strong>\nПожалуйста введите ID Гифта и сумму через двоиточие\nПример: 123:50\nID вашего Гифта: <strong>%s</strong>'
    },
    'txid_in_use': {
        'en': 'TxID/ID already in use',
        'ru': 'TxID/ID уже используется'
    },
}


payment_msg = {
    # Choose Pament method
    'method': {
        'en': '''
Payment for <strong>%s</strong>
Choosen amount <strong>%s</strong>
Total price including discount would be <strong>%s</strong> <strong>%s</strong>

<strong>NOTE:</strong> paying with <strong>Crypto</strong> charges zero fees. 
Crypto Payments are fast and safe way to send crypto.

<strong>PayPal's</strong> payment processing rates range from <strong>1.9%% to 3.5%%</strong> of each transaction, plus a fixed fee ranging from <strong>5 cents to 49 cents</strong>. The exact amount you pay depends on which PayPal product you use
''',
        'ru': '''
Оплата <strong>%s</strong>
Выбранная сумма <strong>%s</strong>
Общая цена, включая скидку, составит <strong>%s</strong> <strong>%s</strong>.

<strong>ПРИМЕЧАНИЕ.</strong> при оплате с помощью <strong>Crypto</strong> комиссия не взимается.
Криптоплатежи — это быстрый и безопасный способ отправки криптовалюты.

Тарифы на обработку платежей <strong>PayPal</strong> варьируются от <strong>1,9%% до 3,5%%</strong> от каждой транзакции плюс фиксированная комиссия в размере от <strong>5 до 49 центов</strong>. Точная сумма, которую вы платите, зависит от того, какой продукт PayPal вы используете.
        '''
    },
    
    # Choose Pament address
    'address': {
        'en': 'Choose desirable address',
        'ru': 'Выберите желаемый адрес'
    },
    
    # When Pament address has been chosen
    'complete': {
        
        'PayPal': {
            'en': '''
Billing address: <strong>%s</strong>

<strong>NOTE.</strong> You need to attach payment ID to your order
To do this, go to <strong>"Profile" > "My Gifts" > "Pending"</strong>, select your order and specify your payment ID

We will then notify you that the payment has been received and send you a gift code.

<strong>%s</strong>
Selected amount <strong>%s</strong>
The total price, including discount, will be
<strong>%s</strong> <strong>%s</strong>.
            ''',
            'ru': '''
Платежный адрес: <strong>%s</strong>

<strong>ПРИМЕЧАНИЕ.</strong> К заказу необходимо добавить ID платежа.
Для этого перейдите в раздел <strong>"Профиль" > "Мои подарки" > "В ожидании"</strong>, выберите свой заказ и укажите свой ID платежа.

Затем мы уведомим вас о получении платежа и отправим вам подарочный код.

<strong>%s</strong>
Выбранная сумма <strong>%s</strong>
Общая стоимость с учетом скидки составит
<strong>%s</strong> <strong>%s</strong>.
            '''  
        },
        
        'Crypto': {
            'en': '''
Billing address: <strong>%s</strong>
Or use the <strong>QR-code</strong> above

<strong>NOTE.</strong> After the transaction, you will receive <strong>TxID</strong> or <strong>transaction ID</strong>, which must be attached to the order.
(<strong>TxID</strong> consists of Latin letters and numbers, for Binance only numbers)
To do this, go to <strong>"Profile" > "'Pending' Gifts
"</strong>, select your order and specify TxID

We will then notify you that the payment has been received and send you a gift code.
Also, by specifying <strong>TxID</strong>, we will send you a link where you can track your transaction

<strong>%s</strong>
Selected amount <strong>%s</strong>
The total price, including discount, will be
<strong>%s</strong> <strong>%s</strong>.   
Price in <strong>%s</strong> at current rate <strong>%s</strong>
(When paying, you can change the amount depending on the current exchange rate)
            ''',
            'ru': '''
Платежный адрес: <strong>%s</strong>
Или используйте <strong>QR-код</strong> выше

<strong>ПРИМЕЧАНИЕ.</strong> После совершения транзакции вам будет доступен <strong>TxID</strong> или <strong>ID транзакции</strong>, который необходимо прикрепить к заказу.
(<strong>TxID</strong> состоит из латинских букв и цифр, для Binance только цифры)
Для этого перейдите в <strong>"Профиль" > "Гифты 'В ожидании'"</strong>, выберете ваш заказ и укажите <strong>TxID</strong>

После чего мы сообщим вам о получении платежа, и вышлем вам подарочный код.
Так же, указав <strong>TxID</strong> мы вышлем вам ссылку, по которой вы сможете отслеживать свою транзакцию

<strong>%s</strong>
Выбранная сумма <strong>%s</strong>
Общая фиатная цена, включая скидку, составит 
<strong>%s</strong> <strong>%s</strong>.        
Цена в <strong>%s</strong> по текущему курсу <strong>%s</strong>
(При оплате вы можете изменить сумму в зависимотсти от текущего курса)
            '''
        }
    }
}

# on /profile
profile_msg = {
    'user_data': {
        'en': '''
<strong>%s</strong> 

User ID: <strong>%s</strong>
Language: <strong>%s</strong>
Currency: <strong>%s</strong>

Open Orders: <strong>%s</strong>
Completed Orders: <strong>%s</strong>
        ''',
        'ru': '''
<strong>%s</strong>

Идентификатор пользователя: <strong>%s</strong>
Язык: <strong>%s</strong>
Валюта: <strong>%s</strong>

Открытые Гифты: <strong>%s</strong>
Полученые Гифты: <strong>%s</strong>
        '''
    },
    'user_gifts': {
        'en': 'Your %s Gifts',
        'ru': 'Ваши %s Гифты'
    },
    'user_gift_data': {
        'en': '''
<strong>%s</strong>
Selected amount <strong>%s</strong>
The total price, including discount: 
<strong>%s</strong> <strong>%s</strong>.
        ''',
        'ru': '''
<strong>%s</strong>
Выбранная сумма <strong>%s</strong>
Общая стоимость с учетом скидки: 
<strong>%s</strong> <strong>%s</strong>.
        '''
    },
    'payment_identifier': {
        'PayPal': {
            'en': '''
Enter your <strong>PayPal address</strong>
Please enter <strong>Order ID</strong> and <strong>payment ID</strong> separated by a colon\nExample: <strong>OrderID:payment ID</strong>.
Yout Order ID: <strong>%s</strong>
            ''',
            'ru': '''
Введите свой <strong>адрес PayPal</strong>
Введите идентификатор заказа и ID платежа, разделенные двоеточием.\nПример: <strong>OrderID:ID платежа</strong>.
Идентификатор вашего заказа: <strong>%s</strong>
            '''
        },
        'Crypto': {
            'en': '''
Enter your <strong>TxID</strong>
Please enter Order ID and amount separated by a colon\nExample: OrderID:TxID.
Yout Order ID: <strong>%s</strong>

<strong>NOTE</strong>: <strong>TxID</strong> consists of Latin letters and numbers, for Binance only numbers
            ''',
            'ru': '''
Введите свой <strong>TxID</strong>
Введите идентификатор заказа и сумму, разделенные двоеточием\nПример: OrderID:TxID.
Идентификатор вашего заказа: <strong>%s</strong>

<strong>ПРИМЕЧАНИЕ</strong>: <strong>TxID</strong> состоит из латинских букв и цифр, для Binance только цифры
            '''
        }
    },
    'identifier_saved': {
        'PayPal': {
            'en': 'PayPal payment ID saved',
            'ru': 'ID платежа сохранен'
        },
        'Crypto': {
            'en': 'TxID saved',
            'ru': 'TxID сохранен'
        }
    },
    'processing': {
        'en': '''
<strong>%s</strong>

Status: <strong>%s</strong>

Selected amount <strong>%s</strong>
The total price, including discount: 
<strong>%s</strong> <strong>%s</strong>.

%s
        ''',
        'ru': '''
<strong>%s</strong>

Status: <strong>%s</strong>

Выбранная сумма <strong>%s</strong>
Общая стоимость с учетом скидки: 
<strong>%s</strong> <strong>%s</strong>.
%s
        '''
    },
    'complete': {
        'en': '''
<strong>%s</strong>
Gift code: <strong>%s</strong>

Status: <strong>%s</strong> 
Amount <strong>%s</strong>
%s
        ''',
        'ru': '''
<strong>%s</strong>
Код Гифта: <strong>%s</strong>

Статус: <strong>%s</strong>

Выбранная сумма <strong>%s</strong>
Общая стоимость с учетом скидки: 
<strong>%s</strong> <strong>%s</strong>.
%s
        '''
    },
    'track_payment': {
        'en': 'Track your payment: %s',
        'ru': 'Отследить платеж: %s'
    },
    'delete': {
        'en': 'Gift %s was deleted',
        'ru': 'Гифт %s удален'
    }
}

# on /profile
help_msg = {
    'en': '''
        List of commands:
        /start -- restart bot
        /description -- what this bot can do
        /help -- open help center
        /profile -- open profile
        /gifts -- list of gifts
        /currency -- change currency
    ''',
    'ru': '''
        Список команд:
         /start -- перезапустить бота
         /description -- что умеет этот бот?
         /help -- открыть справочный центр
         /profile -- открыть профиль
         /gifts -- список подарков
         /currency -- изменить валюту
    '''
}


unknown_msg = {
    'en': "Sorry '%s' is not a valid command. Please run /help to see available commands",
    'ru': "Извините, '%s' не является допустимой командой. Пожалуйста, напишите /help, чтобы увидеть доступные команды"
}

btns = {
    'gifts': {
        'en': 'Gifts',
        'ru': 'Гифты'
    },
    'profile': {
        'en': 'Profile',
        'ru': 'Профиль'
    },
    'help': {
        'en': 'Help',
        'ru': 'Помощь'
    },
    'contact': {
        'en': 'Contact',
        'ru': 'Контакт'
    },
    'back': {
        'en': 'Back',
        'ru': 'Назад'
    },
    'continue': {
        'en': 'Continue',
        'ru': 'Продолжить'
    },
    'amount': {
        'en': 'Change amount',
        'ru': 'Изменить сумму'
    },
    'pending': {
        'en': '+ address/TxID',
        'ru': '+ адрес/TxID'
    },
    
    
    'terms_of_use': {
        'en': 'Terms of use',
        'ru': 'Условия использования'
    }
}

emoji = {
    'en': '\U0001F1EC\U0001F1E7',
    'ru': '\U0001F1F7\U0001F1FA',
    'settings': '\u2699\uFE0F',
}

operations = {
    0: 'offers',
    1: 'category',
    2: 'subcategory',
    3: 'offer_desc',
    4: 'payment_method',
    5: 'terms_of_use',
    6: 'amount',
    7: 'address',
    8: 'complete',
    9: 'user_gifts',
    10: 'delete',
    11: 'sender_payment_data',
}
