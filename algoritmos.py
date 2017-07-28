import datetime
import time
from helpers import graphs
from ibapi.ticktype import TickTypeEnum
from ibapi.contract import Contract
from ibapi.order import Order
from src.ibapy import Ibapy
from helpers.utils import *


class DatosHistoricos(Ibapy):

    def start(self, valid_id):

        contract = Contract()
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"
        contract.symbol = "EUR"

        self.historical_data_req(contract)

    def historical_data_end(self, reqId, historical_data, start, end):
        graphs.candlestick_plot(historical_data)


class DatosLive(Ibapy):

    contract = Contract()

    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    contract.symbol = "EUR"

    def start(self, valid_id):
        print("market data")
        self.market_data_req(self.contract)
        # self.historical_data_req(self.contract, keep_up_to_date=True)

    def tickPrice(self, reqId, tickType, price: float,
                  attrib):
        if tickType == 1:
            print("bid price", datetime.datetime.now(), tickType, price)

    def historicalDataUpdate(self, req_id, bar):
        print(req_id, bar)
"""
    def tick_updated(self, dataType: str, reqId: int, tickType: int, size: float):

        if TickTypeEnum.to_str(tickType) == "ASK":
            print(TickTypeEnum.to_str(tickType), tickType, size)
            if self.price_reference is None:
                self.price_reference = size
                print("reference price:", self.price_reference)
                return
            if size > self.price_reference + 0.00002:
                if self.order.action == "SELL":
                    self.make_order()
            elif size < self.price_reference - 0.00002:
                if self.order.action == "BUY":
                    self.make_order()

    def make_order(self):

        self.placeOrder(self.valid_id, self.contract, self.order)
        self.order.action = "SELL" if self.order.action == "BUY" else "SELL"
        self.valid_id += 1
"""

class KeepUpdatedData(Ibapy):
    contract = Contract()
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    contract.symbol = "EUR"

    def start(self, req_id):
        #self.historical_data_req(self.contract, keep_up_to_date=True)
        self.reqMktData(self.valid_id, self.contract, "", False, False, [])

    def historical_data_end(self, reqId, historical_data, start, end):
        self.graph = graphs.candlestick_plot(historical_data)

    def historicalDataUpdate(self, reqId: int, bar):
        print(bar)



class SimpleBuy(Ibapy):

    contract = Contract()
    order = Order()

    def start(self, valid_id):

        self.contract.secType = "CASH"
        self.contract.currency = "USD"
        self.contract.exchange = "IDEALPRO"
        self.contract.symbol = "EUR"

        self.order.action = "SELL"
        self.order.orderType = "MKT"
        self.order.totalQuantity = 20000

        self.place_order(self.contract, self.order)


class GetData(Ibapy):

    contract = Contract()
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    contract.symbol = "EUR"

    def start(self, valid_id):
        query_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
        self.historical_data_req(self.contract, query_time, "15 D", "1 hour", "MIDPOINT")

    def historical_data_end(self, reqId, historical_data, start, end):
        """
        candles_array = CandlesArray()
        candles_array.data = historical_data
        """
        def req(i):
            return i, datetime.datetime.fromtimestamp(self.time(i)), self.close(i)

        for i in range(len(historical_data)-1, 0, -1):
            print(req(i))


class ContinousData(Ibapy):

    contract = Contract()
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    contract.symbol = "EUR"

    def start(self, valid_id):
        self.watch_product(self.contract)
