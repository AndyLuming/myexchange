import fire
import requests
from kline.agent import KLineAgent
from common.constants import*
from common.apis import*
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
    print('fetch', mySymbol, 'data interval is', myInterval)
    data = kAgent.fetchData(mySymbol, myInterval)

class Observer(object):

  def run(self, symbol, interval):
    global mySymbol
    global myInterval
    mySymbol   = symbol
    myInterval = interval
    url = api_wss + symbol.lower() + '@kline_' + interval
    print('kline url is: ', url)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url, on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
  fire.Fire(Observer)