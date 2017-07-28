"""
Cliente con funcionalidad adicional
"""
from ibapi.client import EClient
from helpers.utils import *
from ibapi.common import *


class Clyent(EClient):
    """
    Implementacion aumentada de EClient
    """
    def __init__(self):
        EClient.__init__(self, wrapper=self)
        self.cly_history = []
        self.valid_id = None

    def valid_id_req(self):
        self.reqIds(-1)

    @request
    def market_data_req(self, contract, snapshot_mode=False, req_id=None):
        valid_id = req_id if req_id else self.valid_id
        self.reqMktData(valid_id, contract, "", snapshot_mode, False, [])
        return req_id

    @request
    def historical_data_req(self, 
                            contract,
                            end_date_time="",
                            duration="1800 S",
                            bar_size_setting="1 secs",
                            what_to_show="MIDPOINT",
                            keep_up_to_date=False,
                            req_id=None):
        """
        Solicita al TWS el envío de todos los ticks en un período determinado de tiempo a un
        ancho de barra determinado.
        duration válidos:
            S	Seconds
            D	Day
            W	Week
            M	Month
            Y	Year
        barSizeSetting válidos:
            1 secs	5 secs	10 secs	15 secs	30 secs
            1 min	2 mins	3 mins	5 mins	10 mins	15 mins	20 mins	30 mins
            1 hour	2 hours	3 hours	4 hours	8 hours
            1 day
            1 week
            1 month
        whatToShow validos:
            TRADES
            MIDPOINT
            BID
            ASK
            BID_ASK
            HISTORICAL_VOLATILITY
            OPTION_IMPLIED_VOLATILITY
            REBATE_RATE
            FEE_RATE
            YIELD_BID
            YIELD_ASK
            YIELD_BID_ASK
            YIELD_LAST
        :param contract: (Contract)
        :param endDateTime:  tiempo final del array a solicitar. El formato es "%Y%m%d %H:%M:%S"
        :param durationString: cantidad de muestras anteriores a devolver dependiendo de barSizeSetting
        :param barSizeSetting: ancho de barra de las velas
        :param whatToShow: valor que se desea consultar
        :return:
        """
        if type(end_date_time) == datetime.datetime:
            end_date_time = datetime_to_str(end_date_time)

        valid_id = req_id if req_id else self.valid_id
        self.reqHistoricalData(valid_id, contract, end_date_time,
                               duration, bar_size_setting, what_to_show,
                               1, 1, keep_up_to_date, [])
        return req_id

    def place_order(self, contract, order, req_id=None):
        valid_id = req_id if req_id else self.valid_id
        self.placeOrder(valid_id, contract, order)
        return req_id

    def go(self):
        try:
            self.connect("127.0.0.1", 7497, clientId=0)
            print("serverVersion:%s connectionTime:%s" % (self.serverVersion(),
                                                          self.twsConnectionTime()))

            # run
            self.run()
        except:
            raise
        finally:
            print("Ibapy finallyzed")
            # app.dumpTestCoverageSituation()
            # app.dumpReqAnsErrSituation()
