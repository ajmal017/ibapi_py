from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as datetime
from .utils import *


def candlestick_plot(data: np.ndarray):
    assert type(data) == np.ndarray, "la data debe ser del tipo numpy.ndarray"
    fig, ax = plt.subplots()
    candlestick2_ohlc(ax, data['open'], data['high'], data['low'], data['close'], width=0.6)

    xdate = [datetime.datetime.fromtimestamp(i) for i in data['time']]

    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

    def mydate(x,pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

    fig.autofmt_xdate()
    fig.tight_layout()

    plt.show()
