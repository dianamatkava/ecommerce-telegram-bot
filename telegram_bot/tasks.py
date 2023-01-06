import json
import requests
from config import paxful_links
from utils import generate_url

DOMAIN = paxful_links['domain']

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': '*/*'
}
def getPaxfullOffers():
    offer_conf = paxful_links['offers']
    for action in offer_conf['url']['action']:
        URL = generate_url(
            [DOMAIN, action, offer_conf['url']['payment_method']],
            offer_conf['params']
        )
        print(URL)
        res = requests.get(URL, headers=headers, verify=False)
        # res = requests.get('https://paxful.com/rest/v1/offers?transformResponse=camelCase&user_badges%5B0%5D=1&user_badges%5B1%5D=2&user_badges%5B2%5D=8&user_badges%5B3%5D=7&user_badges%5B4%5D=6&user_badges%5B5%5D=5&withFavorites=true&crypto_currency_id=1&is_payment_method_localized=0&visitor_country_has_changed=false&users_country_iso=WORLDWIDE&visitor_country_iso=WORLDWIDE&group=gift-cards&payment-method%5B0%5D=with-any-payment-method&type=sell', headers=headers)
        # if res.status_code == 200:
        #     print(json.dumps(res.text, indent=4))
        # else:
        #     print(res.text)
        # print(res.status_code)

getPaxfullOffers()

https://paxful.com/rest/v1/offers?transformResponse=camelCase&user_badges%5B0%5D=1&user_badges%5B1%5D=2&user_badges%5B2%5D=8&user_badges%5B3%5D=7&user_badges%5B4%5D=6&user_badges%5B5%5D=5&withFavorites=true&crypto_currency_id=1&is_payment_method_localized=0&visitor_country_has_changed=false&users_country_iso=WORLDWIDE&visitor_country_iso=WORLDWIDE&group=gift-cards&payment-method%5B0%5D=with-any-payment-method&type=sell

https://paxful.com/sell-tether/with-any-payment-method?transformResponse=camelCase&user_badges%5B0%5D=1&user_badges%5B1%5D=2&user_badges%5B2%5D=8&user_badges%5B3%5D=7&user_badges%5B4%5D=6&user_badges%5B5%5D=5&withFavorites=true&crypto_currency_id=1&is_payment_method_localized=0&visitor_country_has_changed=false&users_country_iso=WORLDWIDE&visitor_country_iso=WORLDWIDE&group=gift-cards&payment-method%5B0%5D=with-any-payment-method&type=sell