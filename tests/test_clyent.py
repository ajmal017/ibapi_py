import pytest
from src.clyent import Clyent
from helpers.utils import *


def test_market_data_req(monkeypatch):
    def reqMktData(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    monkeypatch.setattr(Clyent, "reqMktData", reqMktData)

    clyent = Clyent()
    clyent.valid_id = 11
    clyent.args = None
    clyent.kwargs = None

    assert clyent.market_data_req("contract") == 11

    assert clyent.args[0] == 11
    assert clyent.args[1] == "contract"
    assert clyent.valid_id == 12

    assert clyent.market_data_req("contract", req_id=10)
    assert clyent.args[0] == 10


def test_historical_data_req(monkeypatch):
    def reqHistoricalData(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    monkeypatch.setattr(Clyent, "reqHistoricalData", reqHistoricalData)

    clyent = Clyent()
    clyent.valid_id = 12
    clyent.args = None

    assert clyent.historical_data_req(
        "contract",
        "endDateTime",
        "durationString",
        "barSizeSetting",
        "whatToShow") == 12

    assert clyent.args[0] == 12
    assert clyent.args[1] == "contract"
    assert clyent.args[2] == "endDateTime"
    assert clyent.args[3] == "durationString"
    assert clyent.args[4] == "barSizeSetting"
    assert clyent.args[5] == "whatToShow"
    assert clyent.valid_id == 13
