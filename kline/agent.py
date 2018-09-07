import requests
from kline.candle import Candle
from common.apis import api_kline
from common.constants import DEFAULT_CANDLES_LIMIT

class KLineAgent(object):
    
    def __init__(self):
        pass

    def fetchData(self, symbol, interval, limit = DEFAULT_CANDLES_LIMIT):
        payload = {'symbol': symbol, 'interval': interval, 'limit': limit}
        r = requests.get(api_kline, params=payload)
        print(r.url)
        return r.text
    
    def fetchDataToCandles(self, symbol, interval, limit = DEFAULT_CANDLES_LIMIT):
        payload = {'symbol': symbol, 'interval': interval, 'limit': limit}
        r = requests.get(api_kline, params=payload)
        print(r.url)
        json_array = r.json()
        print(json_array)
        store_list = []
        for item in json_array:
            candle = Candle(high=item[2], open=item[1], low=item[3], close=item[4], volume=item[5], time=item[0], quote_asset_volume=item[7])
            store_list.append(candle)
        
        return store_list