import json
import ast
import pandas as pd
import requests
from config import paxful_conf
from utils import generate_url

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
        print(URL)
        res = requests.get(URL, headers=HEADERS, verify=False)
        if res.status_code == 200:
            temp = ast.literal_eval(
                res.text
                .replace('null', "'null'")
                .replace('false', "'false'")
                .replace('true', "'true'")
                .replace('\/', "/")
            )['data']
            tag_conf = paxful_conf['tags']
            tag_conf['params']['crypto_currency_id'] = id
            # EN_TAG_URL = generate_url(
            #     [DOMAIN, tag_conf['url']['lang']['en'], tag_conf['url']['dir']],
            #     [tag_conf['params']['crypto_currency_id']]
            # )
            # RU_TAG_URL = generate_url(
            #     [DOMAIN, tag_conf['url']['lang']['ru'], tag_conf['url']['dir']],
            #     [tag_conf['params']['crypto_currency_id']]
            # )
            # res = requests.get(EN_TAG_URL, headers=HEADERS)
            # if res.status_code == 200:
            #     pass
            # else:
            #     print(f'Error {res.status_code}: Data for tags was not found {code}')
            #     return res.status_code
        else:
            print(f'Error {res.status_code}: Data was not found for {code}')
            return res.status_code


def updateTags():
    pass

def updateCategories():
    EN_CAT_URL = generate_url(
        [DOMAIN, tag_conf['url']['lang']['en'], tag_conf['url']['dir']],
        [tag_conf['params']['crypto_currency_id']]
    )
    RU_CAT_URL = generate_url(
        [DOMAIN, tag_conf['url']['lang']['ru'], tag_conf['url']['dir']],
        [tag_conf['params']['crypto_currency_id']]
    )

updatePaxfullOffers()
