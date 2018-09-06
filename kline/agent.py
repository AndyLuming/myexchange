import requests
from kline.candle import Candle
from common.apis import api_kline

class KLineAgent(object):
    
    def __init__(self):
        pass

    def fetchData(self, symbol, interval):
        payload = {'symbol': symbol, 'interval': interval}
        r = requests.get(api_kline, params=payload)
        return r.text
    
    def fetchDataToCandles(self, symbol, interval):
        payload = {'symbol': symbol, 'interval': interval}
        r = requests.get(api_kline, params=payload)
        json_array = r.json()
        store_list = []
        for item in json_array:
            candle = Candle(high=item[2], open=item[1], low=item[3], close=item[4], volume=item[5], time=item[0], quote_asset_volume=item[7])
            store_list.append(candle)
        
        return store_list