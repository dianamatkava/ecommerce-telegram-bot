paxful_conf = {
    'domain': 'https://paxful.com',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
    },
    'crypto_currency_id': {
        'BTC': 1,
        'USDT': 4
    },
    'sell': {
        'url': {
            'dir': 'rest/v1/offers'
        },
        'params': {
            'transformResponse':'camelCase',
            'user_badges%5B0%5D':1,
            'user_badges%5B1%5D':2,
            'user_badges%5B2%5D':8,
            'user_badges%5B3%5D':7,
            'user_badges%5B4%5D':6,
            'user_badges%5B5%5D':5,
            'crypto_currency_id': int,
            'withFavorites':'true',
            'is_payment_method_localized':0,
            'visitor_country_has_changed':'true',
            'users_country_iso':'WORLDWIDE',
            'visitor_country_iso':'WORLDWIDE',
            'group':'gift-cards',
            'payment-method%5B0%5D':'with-any-payment-method',
            'type':'sell'
        }
    },
    'categories': {
        'url': {
            'lang': {
                'en': None,
                'ru': 'ru'
            },
            'dir': 'rest/v1/gift-cards/categories'
        }
    },
    'subcategory': {
        'url': {
            'lang': {
                'en': None,
                'ru': 'ru'
            },
            'dir': 'rest/v1/gift-cards/payment-methods'
        },
        'params': {
            'crypto_currency_id': 1
        }
    },
    'tags': {
        'url': {
            'dir': 'rest/v1/tags?transformResponse=camelCase&group=gift-cards&payment-method%5B0%5D=with-any-payment-method'
        }
    }
}

tags = {

}

# Needs rarely update
categories = [
    {
        "id": 1,
        "categoryName": "Food and restaurants",
        "slug": "food_beverage_and_restaurants",
        "optionsCount": 19
    },
    {
        "id": 2,
        "categoryName": "Gaming",
        "slug": "gaming",
        "optionsCount": 12
    },
    {
        "id": 3,
        "categoryName": "Movies and entertainment",
        "slug": "movies_and_entertainment",
        "optionsCount": 8
    },
    {
        "id": 4,
        "categoryName": "Department stores / retail",
        "slug": "apparel_and_sportswear",
        "optionsCount": 17
    },
    {
        "id": 5,
        "categoryName": "Electronics",
        "slug": "tech_and_office",
        "optionsCount": 8
    },
    {
        "id": 6,
        "categoryName": "Travel, Taxi and Destinations",
        "slug": "travel_taxi_and_destinations",
        "optionsCount": 10
    },
    {
        "id": 7,
        "categoryName": "Mobile Refills",
        "slug": "mobile_refills",
        "optionsCount": 5
    },
    {
        "id": 8,
        "categoryName": "Prepaid credit cards",
        "slug": "prepaid_credit_cards",
        "optionsCount": 10
    },
    {
        "id": 9,
        "categoryName": "Online shopping and Retail",
        "slug": "online_shopping_and_retail",
        "optionsCount": 21
    },
    {
        "id": 10,
        "categoryName": "Beauty",
        "slug": "beauty",
        "optionsCount": 4
    },
    {
        "id": 11,
        "categoryName": "Other",
        "slug": "other_gambling",
        "optionsCount": 8
    }
]

payment_conf = {
    'success': {
        'en': '''
Received payment for 
<strong>%s</strong>

Amount: <strong>%s</strong> <strong>%s</strong>
<strong>%s</strong> amount: <strong>%s</strong>

You will receive your Gift code within 15-30 min
        ''',
        'ru': '''
Получена оплату за
<strong>%s</strong>

Сумма: <strong>%s</strong> <strong>%s</strong>
<strong>%s</strong> сумма: <strong>%s</strong>

Вы получите свой подарочный код в течение 15-30 мин.
        '''
    },
    'fail': {
        'en': '''
Received payment for 
<strong>%s</strong>

Amount: <strong>%s</strong> <strong>%s</strong>
<strong>%s</strong> amount: <strong>%s</strong>

Amount is not correct
        ''',
        'ru': '''
Получена оплату за
<strong>%s</strong>

Сумма: <strong>%s</strong> <strong>%s</strong>
<strong>%s</strong> сумма: <strong>%s</strong>

Сумма недостаточна
        '''
    }
}

admin_payment_conf = {
    'payment': '''
Received payment for 
<strong>%s</strong>
ID: <strong>%s</strong>

Amount: <strong>%s</strong> <strong>%s</strong>
<strong>%s</strong> amount: <strong>%s</strong>
Status: <strong>%s</strong>
    '''
}