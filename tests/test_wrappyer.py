from src.wrappyer import Wrappyer
from helpers.utils import *
from ibapi.common import BarData


def test_historical_data(monkeypatch):
    def historical_data(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    monkeypatch.setattr(Wrappyer, "historical_data",
                        historical_data)

    wrappyer = Wrappyer()
    wrappyer.args = None

    test_id = 0

    bar_data = BarData()
    bar_data.date='20120101 00:00:00'
    bar_data.open=2.0
    bar_data.high=3.0
    bar_data.low=4.0
    bar_data.close=5.0
    bar_data.volume= 6 
    bar_data.barCount=7 
    bar_data.average=8.0

    wrappyer.historicalData(test_id, bar_data)
    assert wrappyer.args == (test_id, bar_data)
    hist_data = wrappyer.wr_hist_data[test_id]
    assert len(hist_data) == 1
    assert hist_data['time'][0] == time_to_secs(datetime.datetime(2012, 1, 1))
    assert hist_data['open'][0] == 2.0
    assert hist_data['high'][0] == 3.0
    assert hist_data['low'][0] == 4.0
    assert hist_data['close'][0] == 5.0

    
    bar_data.date = '20120102 00:00:00'
    bar_data.open = 22.0
    bar_data.high = 32.0
    bar_data.low = 42.0
    bar_data.close = 52.0
    bar_data.volume = 62
    bar_data.barCount = 72
    bar_data.average = 82.0

    wrappyer.historicalData(test_id, bar_data)

    assert wrappyer.args == (test_id, bar_data)
    hist_data = wrappyer.wr_hist_data[test_id]
    assert len(hist_data) == 2
    assert hist_data['time'][1] == time_to_secs(datetime.datetime(2012, 1, 2))
    assert hist_data['open'][1] == 22.0
    assert hist_data['high'][1] == 32.0
    assert hist_data['low'][1] == 42.0
    assert hist_data['close'][1] == 52.0


def test_historical_data_end(monkeypatch, g_historical_data):
    def historical_data_end(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    monkeypatch.setattr(Wrappyer, "historical_data_end", historical_data_end)

    wrappyer = Wrappyer()
    wrappyer.args = None

    candles_array_probe = CandlesArray()
    req_id = 0
    hist_data = g_historical_data(nbars=3)
    for record in hist_data:
        record = tuple(record)
        dt = datetime.datetime.fromtimestamp(record[0]).strftime("%Y%m%d %H:%M:%S")
        open_, high, low, close = record[1:]

        bar_data = BarData()
        bar_data.date = dt
        bar_data.open = open_
        bar_data.high = high
        bar_data.low = low
        bar_data.close = close
        bar_data.volume = -1
        bar_data.barCount = -1
        bar_data.average = 0

        wrappyer.historicalData(req_id, bar_data)
        candles_array_probe.add_candle(dt, open_, high, low, close)

    assert type(wrappyer.wr_hist_data[req_id]) == CandlesArray
    assert wrappyer.wr_hist_data[req_id] == candles_array_probe


def test_start(monkeypatch):

    def start(self, valid_id):
        self.args = valid_id

    monkeypatch.setattr(Wrappyer, "start", start)

    wrappyer = Wrappyer()
    wrappyer.args = None

    wrappyer.nextValidId(123)
    assert wrappyer.args == 123
    assert wrappyer.valid_id == 123


def test_nextValidId(monkeypatch):

    def start(self, *args):
        self.args = self.valid_id

    monkeypatch.setattr(Wrappyer, "start", start)

    wrappyer = Wrappyer()
    wrappyer.args = None

    wrappyer.nextValidId(123)
    assert wrappyer.args == 123


def test_historical_data_update():
    """
    La prueba consiste en simular la llegada de una nueva barra
    a través de historicalDataUpdated.

    Debido a que historicalDataUpdated retorna unidades de fecha repetidas
    (fiel a la premisa de que el ancho de la barra es fijo)
    si ocurre alguna actualizacion de barra en un espacio de tiempo menor al
    establecido como mínimo, enviará una vela de fecha repetida pero con datos
    más recientes.

    Esta prueba pretende asegurar que si la fecha es repetida, la nueva barra
    no se adicione sino que sustituya la ultima vela.
    """
    wrappyer = Wrappyer()
    wrappyer.historical_data_init(0)

    bar = fill_bar(
        '20120102 00:00:01',
        22.0, 42.0, 12.0,
        32.0, 62, 72, 82.0
    )
    wrappyer.historicalDataUpdate(0, bar)

    assert len(wrappyer.get_historical_data(0)) == 1
    test_carray = CandlesArray()
    test_carray.add_candle(*unpack_bar(bar))
    assert (wrappyer.get_historical_data(0)[-1] ==
            test_carray[-1])

    # Asegurar que si el ultimo datetime se repite,
    # se sustituye el ultimo elemento de la lista
    bar = fill_bar(
        '20120102 00:00:02',
        12.0, 32.0, 02.0,
        22.0, 52, 62, 72.0
    )
    wrappyer.historicalDataUpdate(0, bar)

    assert len(wrappyer.get_historical_data(0)) == 2
    test_carray.add_candle(*unpack_bar(bar))
    assert (wrappyer.get_historical_data(0) ==
            test_carray)

    # Si el datetime cambia, el elemento sera
    # agregado como nuevo
    bar = fill_bar(
        '20120102 00:00:02',
        22.0, 42.0, 12.0,
        32.0, 62, 72, 82.0
    )
    wrappyer.historicalDataUpdate(0, bar)

    assert len(wrappyer.get_historical_data(0)) == 2
    test_carray = CandlesArray()
    test_carray.add_candle(*unpack_bar(bar))
    assert (wrappyer.get_historical_data(0)[-1] ==
            test_carray[-1])
