import fire
import requests
import json
from kline.agent import KLineAgent
from kline.candle import Candle
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
    data   = json.loads(message)
    if data['e'] == 'kline' and data['s'].lower() == symbol_cache.lower():
        if len(candles_cache) > 0:
            k = data['k']
            candle = Candle(high=k['h'], open=k['o'], low=k['l'], close=k['c'], volume=k['v'], time=k['t'], quote_asset_volume=k['q'])
            previousCandle = candles_cache[len(candles_cache) - 1]
            if previousCandle.time == candle.time:
                candles_cache.pop()
                candles_cache.append(candle)
                print('replace candle', previousCandle, 'with', candle)
            else:
                candles_cache.append(candle)
                print('append new candle', candle)
        else:
            print('candle list is empty')
    else:
        print('Data not match, drop')
    
    if len(candles_cache) > 0:
        last_candle = candles_cache[len(candles_cache) - 1]
        print('time', last_candle.time, 'close', last_candle.close)
           

def on_error(ws, error):
    print(error)

def on_close(ws):
    print('### closed ###')

def on_open(ws):
    print('### opend ###')
    kAgent  = KLineAgent()
    print('fetch', symbol_cache.upper(), 'data interval is', interval_cache)
    candles = kAgent.fetchDataToCandles(symbol_cache.upper(), interval_cache)
    update_candles(candles)

def update_symbol(symbol):
    global symbol_cache
    symbol_cache = symbol

def update_interval(interval):
    global interval_cache
    interval_cache = interval

def update_candles(candles):
    global candles_cache
    candles_cache = candles

class Observer(object):

  def run(self, symbol, interval):
    update_symbol(symbol)
    update_interval(interval)
    update_candles([])
    url = api_wss + symbol.lower() + '@kline_' + interval
    print('kline url is: ', url)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url, on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
  fire.Fire(Observer)