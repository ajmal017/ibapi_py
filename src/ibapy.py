"""
Funcionalidad personalizada para la API
"""
from src.clyent import Clyent
from src.wrappyer import Wrappyer
from ibapi.utils import iswrapper
from ibapi.ticktype import *
from helpers.utils import *
from ibapi.common import *


class Ibapy(Clyent, Wrappyer):
    """
    Modificaciones necesarias para generar las interacciones deseadas
    por el usuario
    """
    def __init__(self):
        Wrappyer.__init__(self)
        Clyent.__init__(self)
        self.req_params = {}
        self.req_queue = RequestsQueue()

    @iswrapper
    def connectAck(self):
        self.startApi()
        self.valid_id_req()

    def time(self, index, req_id=None):
        return self.get_historical_data(req_id)["time"][-1 - index]

    def open(self, index, req_id=None):
        return self.get_historical_data(req_id)["open"][-1 - index]

    def high(self, index, req_id=None):
        return self.get_historical_data(req_id)["high"][-1 - index]

    def low(self, index, req_id=None):
        return self.get_historical_data(req_id)["low"][-1 - index]

    def close(self, index, req_id=None):
        return self.get_historical_data(req_id)["close"][-1 - index]

    def watch_product(self, contract):
        def req_mkt_data(self, valid_id, contract):
            self.expect_mkt_data(valid_id)
            self.market_data_req(contract, valid_id=valid_id)

        valid_id = self.historical_data_req(contract)
        self.req_queue.add(valid_id,
                           "tick_updated",
                           "historicalDataEnd",
                           lambda: req_mkt_data(self, valid_id, contract))

    @virtual
    def large_historical_data_end(self):
        pass

    def large_historical_data_req(self, contract):
        self.req_queue.add(valid_id=self.valid_id, target="")