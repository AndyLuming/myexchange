import requests
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
        return r.json