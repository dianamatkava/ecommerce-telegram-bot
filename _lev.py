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
import os
import asyncio
from binance import BinanceSocketManager
from binance.client import AsyncClient
from dotenv import load_dotenv

load_dotenv()


BINANCE_API_KEY = os.getenv('DI_BINANCE_API_KEY', None)
BINANCE_SECRET_KEY = os.getenv('DI_BINANCE_SECRET_KEY', None)


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
                print('_user_account_listener ', msg)


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
    