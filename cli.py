import fire
import requests
import json
from kline.agent import KLineAgent
from kline.candle import Candle
from common.constants import*
from common.apis import*
from market.agent import MarketAgent
import websocket
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
try:
    import thread 
except ImportError:
    import _thread as thread
# import time
# import plotly.plotly as py
# import plotly.graph_objs as go
# import pandas as pd
# pd.core.common.is_list_like = pd.api.types.is_list_like
# import pandas_datareader as web
# from datetime import datetime

def buildGraph():
    opens  = []
    closes = []
    highs  = []
    lows   = []
    times  = []
    for item in candles_cache:
        opens.append(item.open)
        closes.append(item.close)
        highs.append(item.high)
        lows.append(item.low)
        times.append(item.time)
    
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()                  # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%d')      # e.g., 12

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    candlestick2_ochl(ax, opens, closes, highs, lows, width=0.3)
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.show()

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
    
    # if len(candles_cache) > 0 and is_candlestick_open:
    #     buildGraph()
    #     refreshGraph()
           

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
    if is_candlestick_open:
        buildGraph()

def update_symbol(symbol):
    global symbol_cache
    symbol_cache = symbol

def update_interval(interval):
    global interval_cache
    interval_cache = interval

def update_candles(candles):
    global candles_cache
    candles_cache = candles

def update_is_candlestick_open(is_open):
    global is_candlestick_open
    is_candlestick_open = is_open

class Observer(object):

  def run(self, symbol, interval, candlestick_open = False):
    update_symbol(symbol)
    update_interval(interval)
    update_candles([])
    update_is_candlestick_open(candlestick_open)
    url = api_wss + symbol.lower() + '@kline_' + interval
    print('kline url is: ', url)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url, on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
  fire.Fire(Observer)