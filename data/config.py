paxful_conf = {
    'domain': 'https://paxful.com',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*'
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
    'tags': {
        'url': {
            'lang': {
                'en': None,
                'ru': 'ru'
            },
            'dir': 'rest/v1/gift-cards/payment-methods'
        },
        'params': {
            'crypto_currency_id': int
        }
    }
}

tags = {

}
