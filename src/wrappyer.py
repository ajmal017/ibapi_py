"""
Wrapper con funcionalidad adicional
"""
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.ticktype import *
from helpers.utils import *


class Wrappyer(EWrapper):
    """
    Contiene todos los callbacks personalizados de la API. Estos callbacks serán ejecutados
    cuando el TWS retorne data. El callback ejecutado dependerá de la solicitud realizada al
    TWS.
    :param ticks (dict) con los últimos parámetros del tick retornados por el TWS.
            Se actualiza con cada ejecución de tickPrice y tickSize.
    """
    def __init__(self): 
        super().__init__()
        self.wr_ticks = {}
        self.wr_hist_data = {}
        self.wr_started = False
        self.valid_id = None
        self.req_queue = RequestsQueue()
    
    def expect_mkt_data(self, valid_id):
        self.wr_ticks[valid_id] = {}
        for i in range(10):
            self.wr_ticks[valid_id][i] = -1

    @virtual
    def start(self, valid_id):
        """
        Esta funcion será ejecutada al ser recibido un nexValidId.
        """
        pass

    @virtual
    def tick_updated(self, dataType: str, reqId: TickerId, tickType: TickType, value):
        """
        Esta funcion será ejecutada al ser recibido un valor de tick.
        """
        pass

    @virtual
    def historical_data(self, reqId: TickerId, bar_data: BarData):
        """
        Esta función será ejecutada al ser recibido un registro de historicalData
        """
        pass

    @virtual
    def historical_data_end(self, req_Id, historical_data, start, end):
        """
        Esta función será ejecutada al recibir los datos del historicalData
        :param historical_data: (CandlesArray) arreglo de velas configurable
        :param start: (datetime) tiempo del primer item recibido
        :param end: (datetime) tiempo del último item recibido
        """
        pass

    @virtual
    def next_valid_id(self, order_id):
        """
        Esta función será ejecutada al recibir un nuevo número de id válido.
        :param order_id: nuevo número válido para solicitar acciones al TWS
        """
        pass

    def historical_data_updated(self, req_id, data):
        pass

    def nextValidId(self, orderId: int):
        """
        (revisar)
        El TWS responde a la solicitud de nextValidId() con múltiples llamadas a esta función.
        Para evitar la duplicación del callback se revisa si el orderId es nuevo o repetido.
        """
        super().nextValidId(orderId)

        self.valid_id = orderId
        if not self.wr_started:
            self.start(orderId)
            self.wr_started = True
        else:
            self.next_valid_id(orderId)

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)
        if reqId not in self.wr_ticks.keys():
            self.wr_ticks[reqId] = {}
        self.wr_ticks[reqId][tickType] = size
        args = ["size", reqId, tickType, size]
        self.tickUpdated(*args)

    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if reqId not in self.wr_ticks.keys():
            self.wr_ticks[reqId] = {}
        self.wr_ticks[reqId][tickType] = price
        args = ["price", reqId, tickType, price]
        self.tickUpdated(*args)

    @response
    def tickUpdated(self, *args):
        self.tick_updated(*args)

    def tickSnapshotEnd(self, reqId:int):
        super().tickSnapshotEnd(reqId)
        self.req_queue.process(valid_id=reqId,
                               target="tick_updated").action()
        tick = self.wr_ticks[reqId]
        data = self.wr_hist_data[reqId]
        self.wr_hist_data[reqId].add_candle(datetime.datetime.now(), 
                                            data.open(0),
                                            tick[6],
                                            tick[7],
                                            # (Ask + Bid) / 2
                                            (tick[1] + tick[2]) / 2                                            
                                            )

    def headTimestamp(self, reqId:int, headTimestamp:str):
        print("head time stamp: %s" % headTimestamp)

    def historical_data_init(self, req_id):
        self.wr_hist_data[req_id] = CandlesArray()

    @response
    def historicalData(self, req_id: TickerId , bar_data: BarData):
        super().historicalData(req_id, bar_data)
        date = datetime.datetime.strptime(bar_data.date, "%Y%m%d %H:%M:%S")
        try:
            self.wr_hist_data[req_id]
        except KeyError:
            self.historical_data_init(req_id)

        self.wr_hist_data[req_id].add_candle(
            time_to_secs(date), bar_data.open, bar_data.high, 
            bar_data.low, bar_data.close)
        self.historical_data(req_id, bar_data)

    @response
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        """
        start y end no funcionan correctamente.
        El servidor retorna no retorna la data en el lapso solicitado sino,
        la cantidad de data equivalente a el tiempo solicitado.
        """
        args = [reqId, start, end]
        super().historicalDataEnd(*args)
        new_start = self.wr_hist_data[reqId][0]["time"]
        new_end = self.wr_hist_data[reqId][-1]["time"]

        self.historical_data_end(reqId, self.wr_hist_data[reqId].data, new_start, new_end)
        try:
            self.req_queue.process(valid_id=reqId,
                                target="historicalDataEnd").action()
        except:
            pass

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        """
        Si la barra recibida es de fecha repetida,
        sustituir la vela vieja por la nueva.
        :param reqId: valid_id
        :param bar: vela
        :return:
        """
        super().historicalDataUpdate(reqId, bar)
        if len(self.wr_hist_data[reqId]) == 0:
            """
            Estado inicial vacio, aun no hay data.
            """
            self.wr_hist_data[reqId].add_candle(
                *unpack_bar(bar)
            )
        elif (to_datetime(bar.date) ==
                to_datetime(self.wr_hist_data[reqId][-1]["time"])):
            self.wr_hist_data[reqId].data = \
                np.append(
                    self.wr_hist_data[reqId][:-1],
                    historical_data_to_numpy(
                        [(str_datetime_to_int(bar.date),
                          bar.open,
                          bar.high,
                          bar.low,
                          bar.close)]
                    )
                )
        else:
            self.wr_hist_data[reqId].add_candle(bar.date,
                                                bar.open,
                                                bar.high,
                                                bar.low,
                                                bar.close)
        self.historical_data_updated(reqId, self.wr_hist_data[reqId])

    def get_historical_data(self, req_id=None):
        if req_id is None:
            req_id = max(self.wr_hist_data.keys())
        return self.wr_hist_data[req_id]
