# # ----- TEST PAYPAL API -------

import os
from dotenv import load_dotenv

load_dotenv()
















# # ----- TEST BINANCE API -------


# BINANCE_API_KEY = os.getenv('DI_BINANCE_API_KEY', None)
# BINANCE_SECRET_KEY = os.getenv('DI_BINANCE_SECRET_KEY', None)


# # url = 'https://api.binance.com/api/v3/userDataStream'
# # res = requests.post(url, headers={'X-MBX-APIKEY': BINANCE_API_KEY})
# # print(res.json())
# # listen_key = res.json()['listenKey']


# # url = f"wss://stream.binance.com:9443/ws/{listen_key}"

# # def on_open(ws):
# #     print(f"Connected")

# # def on_message(ws, message):
# #     print(f"Message: {message}")

# # def on_error(ws, error):
# #     print(f"Error: {error}")

# # def on_close(ws, close_status_code, close_msg):
# #     print(f"Close: {close_status_code} {close_msg}")


# # ws = websocket.WebSocketApp(url=url,
# #                             on_open=on_open,
# #                             on_message=on_message,
# #                             on_error=on_error,
# #                             on_close=on_close)
# # ws.run_forever(ping_interval=300)



# # GET (only) wallet info
# from binance.client import Client
# client = Client(
#     BINANCE_API_KEY, 
#     BINANCE_SECRET_KEY
# )

# # manually changing API URL to test API URL
# # client.API_URL = 'https://testnet.binance.vision/api'

# # Returns all currency and its amount in wallet if exist 
# # print(client.get_account())

# # Return amount of specified cur
# # print(client.get_asset_balance(asset='BTC'))


# # Get deposit history
# deposits = client.get_deposit_history(startTime='1674156572611')
# btc_deposits = client.get_deposit_history(coin='BTC')

# print(deposits)

# # # Get withdraws history
# # withdraws = client.get_withdraw_history()
# # btc_withdraws = client.get_withdraw_history(coin='BTC')





# # # Binance Websocket

# # from binance import Client, ThreadedWebsocketManager


# # def handle_socket_message(msg):
# #     print(f"message type: {msg['e']}")
# #     print(msg)


# # twm = ThreadedWebsocketManager()
# # twm.start()
# # twm.start_kline_socket(callback=handle_socket_message, symbol='BNBBTC')
# # twm.join()


# # # OR


# # from binance import ThreadedWebsocketManager


# # symbol = 'BTCUCDT'

# # twm = ThreadedWebsocketManager(
# #     api_key=BINANCE_API_KEY, 
# #     api_secret=BINANCE_SECRET_KEY
# # )
# # # start is required to initialise its internal loop
# # twm.start()

# # def handle_socket_message(msg):
# #     print(msg)

# # # See more streams in Doc
# # twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

# # # multiple sockets can be started
# # twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

# # # or a multiplex socket can be started like this
# # # see Binance docs for stream names
# # streams = ['bnbbtc@miniTicker', 'bnbbtc@bookTicker']
# # twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

# # twm.join()



