import requests
import websocket
from config import BINANCE_API_KEY


url = 'https://api.binance.com/api/v3/userDataStream'
res = requests.post(url, headers={'X-MBX-APIKEY': BINANCE_API_KEY})
listen_key = res.json()['listenKey']

url = f"wss://stream.binance.com:9443/ws/{listen_key}"

def on_open(ws):
    print(f"Connected")

def on_message(ws, message):
    print(f"Message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"Close: {close_status_code} {close_msg}")


ws = websocket.WebSocketApp(url=url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever(ping_interval=300)
