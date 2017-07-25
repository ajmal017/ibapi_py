import pytest
from src.ibapy import Ibapy
from helpers.utils import *


req_id = 0


@pytest.fixture()
def app(historical_data):
    ibapy = Ibapy()
    ibapy.next_valid_id = req_id
    ibapy.wr_hist_data[req_id] = historical_data
    return ibapy


class TestOpen:

    def test_data_exists(self, app):
        assert app.get_historical_data(req_id)["open"] is not None

    def test_returns_a_value(self, app):
        assert app.open(0, req_id) is not None

    def test_returns_the_correct_value(self, app):
        assert app.open(0, req_id) - 1.1 < 0.00001


class TestHigh:

    def test_data_exists(self, app):
        assert app.get_historical_data(req_id)["high"] is not None

    def test_returns_a_value(self, app):
        assert app.high(1, req_id) is not None

    def test_returns_the_correct_value(self, app):
        assert app.high(1, req_id) - 2.2 < 0.00001


class TestLow:

    def test_data_exists(self, app):
        assert app.get_historical_data(req_id)["low"] is not None

    def test_returns_a_value(self, app):
        assert app.low(2, req_id) is not None

    def test_returns_the_correct_value(self, app):
        assert app.low(2, req_id) - 3.3 < 0.00001


class TestClose:
    def test_exists(self, app):
        assert app.get_historical_data(req_id)["close"] is not None

    def test_returns_a_value(self, app):
        assert app.close(3, req_id) is not None

    def test_returns_the_correct_value(self, app):
        assert app.close(3, req_id) - 4.4 < 0.00001


def test_valid_id(monkeypatch):
    def start(self, *args):
        self.args = args

    monkeypatch.setattr(Ibapy, 'start', start)

    ibapy = Ibapy()
    ibapy.args = None

    ibapy.nextValidId(12)

    import datetime
    from ibapi.contract import Contract

    assert ibapy.historical_data_req(
        Contract(), datetime.datetime.now(),
        "15 D", "1 hour", "MIDPOINT") == 12


@pytest.mark.skip("Funcionalidad no implementada")
def test_historical_data_req():
    ibapy = Ibapy()
    ibapy.args = None

    data = CandlesArray()
    d0 = datetime.datetime(2010, 1, 1)
    data.add_candle(d0,
                    1, 2, 3, 4)
    data.add_candle(d0 - datetime.timedelta(seconds=1800),
                    6, 7, 8, 9)

    ibapy.req_params['time_span'] = d0 - \
        datetime.timedelta(days=1)
    ibapy.req_params['contract'] = "contract"

    ibapy.historical_data_end(12, data, data[1], data[0])
    # asegurar que se agrega una funcion a la cola
    assert ibapy.args[0] == "contract"
    assert ibapy.args[1] == d0 - datetime.timedelta(seconds=1800)


def test_watch_product(mck, g_historical_data):
    ibapy = mck(Ibapy, "market_data_req")
    ibapy.valid_id = 0
    ibapy.wr_hist_data = {
        ibapy.valid_id: g_historical_data()
    }
    print(type(ibapy.wr_hist_data))
    contract = "contract"
    assert ibapy.watch_product
    ibapy.watch_product(contract)
    req_queue = ibapy.req_queue
    assert len(req_queue) == 1
    assert req_queue.first.valid_id == 0
    assert req_queue.first.emitter == "watch_product"
    assert req_queue.last.valid_id == 0
    assert req_queue.last.target == "historicalDataEnd"
    ibapy.historicalDataEnd(0, "20100606 00:00:00",
                            "20100606 00:00:00")

    assert len(req_queue) == 1
    assert ibapy.args[0] == contract
    ibapy.tickSnapshotEnd(0)
    assert req_queue.last.target == "marq"
    assert len(req_queue) == 1
    assert ibapy.kwargs["req_id"] == 0
