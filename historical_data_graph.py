from helpers.utils import historical_data_to_numpy, CandlesArray
from helpers.graphs import candlestick_plot, fig, ax
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ohlc
from threading import Thread
from src.ibapy import Ibapy
from ibapi.contract import Contract
import datetime


data = []

class IbGraph(Ibapy):
    contract = Contract()
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    contract.symbol = "EUR"
    graph_data = CandlesArray()

    def start(self, valid_id):
        id_ = self.historical_data_req(self.contract, keep_up_to_date=True)
        self.historical_data_init(id_)
        self.graph_data = self.wr_hist_data[id_]

    def historicalDataUpdate(self, reqId: int, bar):
        self.wr_hist_data[reqId].add_candle(datetime.datetime.now(),
                                            bar.open,
                                            bar.high,
                                            bar.low,
                                            bar.close)
        global data
        data = self.wr_hist_data[reqId].data


def thread1():
    global data
    ibg = IbGraph()
    ibg.go()

thread = Thread(target=thread1)
thread.start()


def func(i):
    if len(data) > 10:
        ax.clear()
        candlestick_plot(data[-50:])

ani = animation.FuncAnimation(fig, func, interval=500)
plt.show()
