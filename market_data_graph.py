import matplotlib.animation as animation
import matplotlib.pyplot as plt
from threading import Thread
from src.ibapy import Ibapy
from ibapi.contract import Contract
import datetime
import logging

logging.basicConfig(level=logging.INFO)

ask_price = []
bid_price = []
mkt_data_time = []

fig, ax = plt.subplots()
ln, = plt.plot(mkt_data_time, bid_price, 'ro', animated=True)

class IbGraph(Ibapy):
    contract = Contract()
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    contract.symbol = "EUR"

    def start(self, valid_id):
        self.expect_mkt_data(valid_id)
        self.reqMktData(valid_id, self.contract, "", True, False, [])
        print("start", valid_id)

    def tickSnapshotEnd(self, reqId:int):
        print("aki")
        global ask_price, bid_price, mkt_data_time
        bid_price.append(self.wr_ticks[reqId][1])
        ask_price.append(self.wr_ticks[reqId][2])
        mkt_data_time.append(0)
        self.reqMktData(reqId, self.contract, "", False, False, [])

    def tick_updated(self, dataType: str, reqId, tickType, value):
        global ask_price, bid_price, mkt_data_time
        if len(bid_price) > 0:
            if tickType == 1:
                bid_price.append(value)
                ask_price.append(ask_price[-1])
                mkt_data_time.append(len(bid_price)-1)
            if tickType == 2:
                bid_price.append(bid_price[-1])
                ask_price.append(value)
                mkt_data_time.append(len(bid_price)-1)


def thread1():
    ibg = IbGraph()
    ibg.go()

thread = Thread(target=thread1)
thread.start()


def func(i):
    global ask_price, bid_price, mkt_data_time
    """
    print(mkt_data_time, bid_price)
    ln.set_data(mkt_data_time, bid_price)
    ln.set_data([0,1,2,3], [0,1,2,3])
    """
    ax.clear()
    ax.plot(mkt_data_time[-20:], bid_price[-20:])
    ax.plot(mkt_data_time[-20:], ask_price[-20:])


ani = animation.FuncAnimation(fig, func, interval=500)
plt.show()