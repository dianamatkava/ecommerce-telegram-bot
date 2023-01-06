paxful_links = {
    'domain': 'https://paxful.com',
    'sell_tether': {
        'url': {
            'dir': 'https://paxful.com/rest/v1/offers'
        },
        'params': {
            'transformResponse':'camelCase',
            'user_badges%5B0%5D':1,
            'user_badges%5B1%5D':2,
            'user_badges%5B2%5D':8,
            'user_badges%5B3%5D':7,
            'user_badges%5B4%5D':6,
            'user_badges%5B5%5D':5,
            'withFavorites':'true',
            'crypto_currency_id':2,
            'is_payment_method_localized':0,
            'visitor_country_has_changed':'false',
            'users_country_iso':'WORLDWIDE',
            'visitor_country_iso':'WORLDWIDE',
            'group':'gift-cards',
            'payment-method%5B0%5D':'with-any-payment-method',
            'type':'sell'
        }
    },
    'categories': {
        'url': {
            'lang': [None, 'ru'],
            'dir': 'rest/v1/gift-cards/categories'
        }
    },
    'sub_categories': {
        'url': {
            'lang': ['', 'ru'],
            'dir': 'rest/v1/gift-cards/categories'
        },
        'params': {
            'crypto_currency_id': {
                'BTC': 1,
                'USDT': 2
            }
        }
    }
}

data = {'transformResponse':'camelCase',
            'user_badges%5B0%5D':1,
            'user_badges%5B1%5D':2,}