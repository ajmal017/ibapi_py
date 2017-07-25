from helpers.utils import *
from helpers.graphs import *


carray = CandlesArray()
carray.add_candle(datetime.datetime.now() - datetime.timedelta(seconds=1), 3, 4, 1, 2)

fig, ax = candlestick_plot(carray.data)

carray.add_candle(datetime.datetime.now() - datetime.timedelta(seconds=0), 4, 5, 2, 3)


def mydate(x, pos):
    try:
        return xdate[int(x)]
    except IndexError:
        return ''


ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

fig.autofmt_xdate()

print("aki")
ax.cla()

# use draw() instead of show() to update the same window
plt.draw()

