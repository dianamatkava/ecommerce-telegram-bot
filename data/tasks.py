import time
import json
import requests
from .config import paxful_conf
from .utils import generate_url, str_to_dict, merge_lang, str2bool
from .models import Category, Tag, Subcategory, Offer, OfferDetail


DOMAIN = paxful_conf['domain']
HEADERS = paxful_conf['headers']


def updatePaxfullOffers():
    sell_conf = paxful_conf['sell']
    cur = paxful_conf['crypto_currency_id']
    data = list()
    for code, id in cur.items():
        sell_conf['params']['crypto_currency_id'] = id
        URL = generate_url(
            [DOMAIN, sell_conf['url']['dir']], sell_conf['params']
        )
        res = requests.get(URL, headers=HEADERS, verify=False)
        if res.status_code == 200:
            data = str_to_dict(res.text)['data']
            default_category = Category.objects.get(name='Other')
            for offer in data:
                if offer['pricePerUsd'] >= 1.1:
                    tags = list()
                    if offer['tags']:
                        ids = [tag['id'] for tag in offer['tags']]
                        tags = Tag.objects.filter(px_id__in=ids)
                    sub_cat_values = {
                        'px_id': 0,
                        'ru_name': offer['paymentMethodName'],
                        'category': default_category
                    }
                    sub_cat, created = Subcategory.objects.get_or_create(
                        name=offer['paymentMethodName'],
                        defaults=sub_cat_values
                    )
                    if created:
                        print(f'Object of {sub_cat} was created')

                    offer_detail_values = {
                        'feedback_negative': offer['feedbackNegative'],
                        'feedback_positive': offer['feedbackPositive'],
                        'predefined_amount': offer['predefinedAmount'],
                        'fiat_amount_range_min': offer['fiatAmountRangeMin'],
                        'fiat_amount_range_max': offer['fiatAmountRangeMax'],
                        'fiat_price_per_btc': offer['fiatPricePerBtc'],
                        'price_per_btc': offer['pricePerBtc'],
                        'fee_percentage': offer['feePercentage'],
                        'payment_method_group_id': offer['paymentMethodGroupId'],
                        'percent_per_usd': offer['percentPerUsd'],
                        'require_full_name_visibility': str2bool(offer['requireFullNameVisibility']),
                        'default_flow_type': offer['defaultFlowType'],
                    }
                    offer_detail, created = OfferDetail.objects.update_or_create(
                        px_id=offer['idHashed'], defaults=offer_detail_values
                    )
                    if created:
                        print(f'Created new obj of {offer_detail}')
                    else:
                        print(f'Updated new obj of {offer_detail}')
                    offer_values = {
                        'sell_cur': offer['cryptoCurrencyCode'],
                        'buy_cur': offer['fiatCurrencyCode'],
                        'margin': offer['margin'],
                        'price_per_cur': offer['pricePerUsd'],
                        'require_verified_id': str2bool(offer['requireVerifiedId']),
                        'category': sub_cat.category,
                        'subcategory': sub_cat,
                        'payment_method_label': offer['paymentMethodLabel'],
                        'username': offer['username'],
                        'score': offer['score'],
                        'last_seen': offer['lastSeenString'],
                        'average_trade_speed': offer['releaseTimeMedianHumanize'],
                        'user_timezone': offer['userTimezone'],
                        'offer_type': offer['offerType'],
                        'offer_detail': offer_detail,
                    }
                    offer, created = Offer.objects.update_or_create(
                        px_id=offer['idHashed'], defaults=offer_values
                    )
                    offer.tags.set(tags)
                    if created:
                        print(f'Created new obj of {offer}')
                    else:
                        print(f'Updated new obj of {offer}')

        else:
            print(f'Error {res.status_code}: Data was not found for {code}')
            return res.status_code


# updatePaxfullOffers()

def updateOfferDescription():
    offers = Offer.objects.all()
    x = 0
    while x != len(offers)-1:
        res = requests.get(
            f'https://paxful.com/offer/{offers[x].px_id}', headers=HEADERS, verify=False
        )
        print(f'[{x+1}] Updating Data for {offers[x].px_id, offers[x].username}\n{offers[x].display_name()}\nStatus Code: {res.status_code}')
        if res.status_code == 200:
            x += 1
            start = res.text.index('offerTerms')
            end = res.text.index('noCoins"')
            desc = str_to_dict('{"' + res.text[start:end][:-2]+'}')
            offers[x].description = desc['offerTerms']
            offers[x].save()
            print(json.dumps(desc, indent=4), '\n')
            time.sleep(1)
        elif res.status_code in [404, 410]:
            offers[x].delete()
            x += 1
        else:
            time.sleep(15)

updateOfferDescription()

def updateTags():
    tag_conf = paxful_conf['tags']
    URL = generate_url([DOMAIN, tag_conf['url']['dir']])
    res = requests.get(URL, headers=HEADERS)
    if res.status_code == 200:
        data = str_to_dict(res.text)['data']
        for tag in data:
            values = {
                'name': tag['name'],
                'description': tag['description'],
                'px_slug': tag['slug'],
            }
            obj, created = Tag.objects.update_or_create(
                px_id=tag['id'], defaults=values
            )
            if created:
                print(f'Created new obj of {obj}')
            else:
                print(f'Updated new obj of {obj}')
    else:
        return 400, f'Error {res.status_code}: Data was not found by {URL}'


def updateSubCategories():
    s_cat_conf = paxful_conf['subcategory']
    EN_S_CAT_URL = generate_url(
        [DOMAIN, s_cat_conf['url']['lang']['en'], s_cat_conf['url']['dir']],
        s_cat_conf['params']
    )
    RU_S_CAT_URL = generate_url(
        [DOMAIN, s_cat_conf['url']['lang']['ru'], s_cat_conf['url']['dir']],
        s_cat_conf['params']
    )
    res = requests.get(EN_S_CAT_URL, headers=HEADERS)
    if res.status_code == 200:
        en_data = str_to_dict(res.text)['data']
        res = requests.get(RU_S_CAT_URL, headers=HEADERS)
        if res.status_code == 200:
            ru_data = str_to_dict(res.text)['data']
            data = merge_lang(en=en_data, ru=ru_data, field='name')
            updateCategories()
            for s_cat in data:
                category = Category.objects.filter(px_id=s_cat['gift_card_category_id']).first()
                if category:
                    values = {
                        'name': s_cat['name'],
                        'ru_name': s_cat['ru_name'],
                        'px_slug': s_cat['slug'],
                        'category': category
                    }
                    obj, created = Subcategory.objects.update_or_create(
                        px_id=s_cat['id'], defaults=values
                    )
                    if created:
                        print(f'Created new obj of {obj}')
                    else:
                        print(f'Updated new obj of {obj}')
                else:
                    print(f'Fatal Error {res.status_code}: Category not found for {s_cat}')
        else:
            return 400, f'Error {res.status_code}: Data was not found by {RU_S_CAT_URL}'
    else:
        return 400, f'Error {res.status_code}: Data was not found by {EN_S_CAT_URL}'


def updateCategories():
    cat_conf = paxful_conf['categories']
    EN_CAT_URL = generate_url(
        [DOMAIN, cat_conf['url']['lang']['en'], cat_conf['url']['dir']]
    )
    RU_CAT_URL = generate_url(
        [DOMAIN, cat_conf['url']['lang']['ru'], cat_conf['url']['dir']]
    )
    res = requests.get(EN_CAT_URL, headers=HEADERS)
    if res.status_code == 200:
        en_data = str_to_dict(res.text)['data']
        res = requests.get(RU_CAT_URL, headers=HEADERS)
        if res.status_code == 200:
            ru_data = str_to_dict(res.text)['data']
            data = merge_lang(en=en_data, ru=ru_data, field='name')
            for category in data:
                values = {
                    'name': category['category_name'],
                    'ru_name': category['ru_name'],
                    'px_slug': category['slug']
                }
                obj, created = Category.objects.update_or_create(
                    px_id=category['id'], defaults=values
                )
                if created:
                    print(f'Created new obj of {obj}')
                else:
                    print(f'Updated new obj of {obj}')
        else:
            return 400, f'Error {res.status_code}: Data was not found by {RU_CAT_URL}'
    else:
        return 400, f'Error {res.status_code}: Data was not found by {EN_CAT_URL}'
# updateTags()
# updateSubCategories()