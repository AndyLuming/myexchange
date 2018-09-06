import requests
from common.apis import api_market

class MarketAgent(object):

    def __init__(self):
        pass

    def fetch_all_market_data(self):
        r = requests.get(api_market)
        return r.text