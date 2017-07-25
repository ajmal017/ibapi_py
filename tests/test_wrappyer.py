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
