# BinanceSocketManager. 
# User Socket. 
# This watches for 3 different user events


# # Deposit
# _user_account_listener  {'e': 'balanceUpdate', 'E': 1674156572611, 'a': 'BTC', 'd': '0.00080000', 'T': 1674156572610}
# _user_account_listener  {'e': 'outboundAccountPosition', 'E': 1674156572611, 'u': 1674156572610, 'B': [{'a': 'BTC', 'f': '0.00080000', 'l': '0.00000000'}]}

# [{'id': '3291658932095273985', 'amount': '0.0008', 'coin': 'BTC', 'network': 'BTC', 'status': 1, 'address': '1LG7NtQ1TMt1styoi3sRuANRjqYuN1Sp4m', 'addressTag': '', 'txId': 'Internal transfer 126744067061', 'insertTime': 1674156561000, 'transferType': 1, 'confirmTimes': '1/1', 'unlockConfirm': 2, 'walletType': 0}]

# # Withdraw
# _user_account_listener  {'e': 'balanceUpdate', 'E': 1674157255424, 'a': 'BTC', 'd': '-0.00079580', 'T': 1674157255423}
# _user_account_listener  {'e': 'outboundAccountPosition', 'E': 1674157255424, 'u': 1674157255423, 'B': [{'a': 'BTC', 'f': '0.00000420', 'l': '0.00000000'}]}


import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'paxfull_gifts.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import asyncio
from binance import BinanceSocketManager
from binance.client import AsyncClient
from dotenv import load_dotenv
from data.models import Payment, PaymentAddress, GiftOrder
from .utils import get_fiat_amount

load_dotenv()


BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', None)
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY', None)


class BinancePayment:
    def __init__(self, async_client: AsyncClient = None):
        self._async_client = async_client

    async def run(self, loop):
        loop.create_task(self._user_account_listener())

    async def _user_account_listener(self):
        bsm = BinanceSocketManager(self._async_client)
        # async with bsm.trade_socket(symbol='BTCUSDT') as us: # USE FOR TESTING
        async with bsm.user_socket() as us:
            while True:
                msg = await us.recv()
                if msg['e'] == 'balanceUpdate':
                    _type = 'Deposit' if float(msg['d']) > 0 else 'Withdraw'
                    transaction = dict()
                    if _type == 'Deposit':
                        transaction = await self._async_client.get_deposit_history(
                            startTime=msg['E'], coin=msg['a']
                        )
                    else:
                        transaction = await self._async_client.get_withdraw_history(
                            startTime=msg['E'], coin=msg['a']
                        )
                    
                    for tr in transaction:
                        address = PaymentAddress.objects.filter(
                            address=tr['address']
                        )
                        user = None
                        fiat_amount = None
                        order = GiftOrder.objects.filter(TxID=tr['txId'])
                        if not order:
                            order = None
                        else:
                            user = order.user
                            if msg['a'] != order.offer.buy_cur:
                                fiat_amount = get_fiat_amount(
                                order.offer.buy_cur, msg['a'], tr['amount']
                            )
                                
                        payment, created = Payment.objects.update_or_create(
                            bc_id=tr['id'],
                            TxID=tr['txId'],
                            defaults={
                                '_type': _type,
                                'status': bool(tr['status']),
                                'insert_time': tr['insertTime'],
                                'amount': tr['amount'],
                                'address': address,
                                'order': order,
                                'tg_user': user,
                                'fiat_amount': fiat_amount,
                                'currency': msg['a']
                            }
                        )
                        if created:
                            print(f'CREATED new payment {payment}')
                print(msg)


async def main():
    async_client = await AsyncClient().create(
        api_key=BINANCE_API_KEY, 
        api_secret=BINANCE_SECRET_KEY
    )

    binance_payment = BinancePayment(async_client)
    loop.create_task(binance_payment.run(loop))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
    