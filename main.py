import requests
from kline.agent import KLineAgent
from common.constants import*
from market.agent import MarketAgent
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print('### closed ###')

def on_open(ws):
    print('### opend ###')
    kAgent  = KLineAgent()
    btcusdt = kAgent.fetchData('BTCUSDT', INTERVAL_MIN_1)
    print(btcusdt)

def main():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream2.binance.cloud/ws/btcusdt@kline_1m", on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
    main()