class Candle(object):

    def __init__(self, high, open, low, close, volume, time, quote_asset_volume):
        self.high               = high
        self.open               = open
        self.low                = low
        self.close              = close
        self.volume             = volume
        self.time               = time
        self.quote_asset_volume = quote_asset_volume