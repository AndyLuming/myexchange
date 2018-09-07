import matplotlib
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY

def show_candle_stick(candles):
    opens  = []
    closes = []
    highs  = []
    lows   = []
    times  = []
    for item in candles:
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