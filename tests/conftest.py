import pytest
from helpers.utils import *


@pytest.fixture()
def historical_data():
    return historical_data_to_numpy(
            [(1498750035, 6.1, 6.2, 6.3, 6.4),
             (1498750034, 5.1, 5.2, 5.3, 5.4),
             (1498750033, 4.1, 4.2, 4.3, 4.4),
             (1498750032, 3.1, 3.2, 3.3, 3.4),
             (1498750031, 2.1, 2.2, 2.3, 2.4),
             (1498750030, 1.1, 1.2, 1.3, 1.4)])


@pytest.fixture()
def g_historical_data():
    def g_candles_array(base_date=datetime.datetime(2010, 1, 1),
                        barsize=datetime.timedelta(seconds=1),
                        nbars=8000):
        candles_array = historical_data_to_numpy(
            [(time_to_secs(base_date + i * barsize),
              i, i + 1, i + 2, i + 3)
             for i in range(nbars)])
        return candles_array
    return g_candles_array


@pytest.fixture()
def mck(monkeypatch):
    def func(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def mocker(cls, method_name: str):
        monkeypatch.setattr(cls, method_name, func)
        cls.args = None
        return cls()

    return mocker


