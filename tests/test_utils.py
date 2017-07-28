import pytest
import time
from helpers.utils import *


test_data = [(10000, 2.0, 3.0, 4.0, 5.0)]


class TestHistoricalDataToNumpy:

    def test_exists(self):
        assert historical_data_to_numpy(test_data) is not None

    def test_gives_correct_value(self):
        assert historical_data_to_numpy(test_data) == \
               np.array(test_data, dtype=[('time', '<i4'), ('open', '<f4'), ('high', '<f4'),
                                          ('low', '<f4'), ('close', '<f4')])


class TestCandlesArray:

    @pytest.fixture()
    def empty_candles_array(self):
        return CandlesArray()

    @staticmethod
    def simulated_candles_array(empty_candles_array: CandlesArray, g_historical_data):
        large_historical_data = g_historical_data()
        candles_array = empty_candles_array
        candles_array.data = large_historical_data
        return candles_array

    def test_creates_an_empty_candle_array(self, empty_candles_array):

        assert empty_candles_array.req_id is None
        assert np.array_equal(empty_candles_array.data, np.array([], dtype=[('time', '<i4'), ('open', '<f4'), ('high', '<f4'),
                                                                            ('low', '<f4'), ('close', '<f4')]))

    def test_add_candles_should_work(self, empty_candles_array: CandlesArray, historical_data):
        candles_array = empty_candles_array
        candles_array.add_candle(*historical_data[0])

        data1 = list(historical_data[1])
        with_time_as_datetime = (
            [datetime.datetime.fromtimestamp(data1[0])] +
            data1[1:]
        )
        candles_array.add_candle(*with_time_as_datetime)
        assert candles_array.data[0] == historical_data[0]
        assert candles_array.data[1] == historical_data[1]

    def test_candles_array_works(self, g_historical_data):
        large_historical_data = g_historical_data()
        start = large_historical_data[0]['time']
        assert large_historical_data is not None
        assert large_historical_data[0]['open'] - 0.1 < 0.000001
        assert large_historical_data[-1]['time'] \
            == start + int(((8000 - 1) * datetime.timedelta(seconds=1)).total_seconds())

    def test_returns_a_nparray(self, empty_candles_array: CandlesArray, g_historical_data):
        large_historical_data = g_historical_data()
        candles_array = empty_candles_array
        bar_changed_historical_data = candles_array.change_bar_size(large_historical_data, datetime.timedelta(hours=1))
        assert type(bar_changed_historical_data) == np.ndarray

    def test_can_change_candle_bar_size_to_1_hour(self, empty_candles_array: CandlesArray, g_historical_data):
        large_historical_data = g_historical_data()
        candles_array = empty_candles_array
        bar_changed_historical_data = candles_array.change_bar_size(large_historical_data, datetime.timedelta(hours=1))
        data = bar_changed_historical_data
        assert data[0]['open'] == 0
        assert data[0]['close'] == 3599 + 3
        assert data[1]['open'] == 3600
        assert len(data) == 3
        assert data[-1]["open"] == 7200
        assert data[-1]["close"] == 7999 + 3

    def test_can_change_candle_bar_size_to_1_minute(self, empty_candles_array: CandlesArray, g_historical_data):
        large_historical_data = g_historical_data()
        candles_array = empty_candles_array
        bar_changed_historical_data = candles_array.change_bar_size(large_historical_data, datetime.timedelta(minutes=1))
        data = bar_changed_historical_data
        assert data[0]['open'] == 0
        assert data[0]['close'] == 59 + 3
        assert data[1]['open'] == 60
        assert data[1]['close'] == 119 + 3
        assert len(data) == 134
        assert data[-1]["open"] == 60 * 133
        assert data[-1]["close"] == 7999 + 3

    def test_time(self, empty_candles_array: CandlesArray, g_historical_data):
        candles_array = self.simulated_candles_array(empty_candles_array, g_historical_data)
        assert candles_array.time(0) == \
            time_to_secs(datetime.datetime(2010, 1, 1) +
                         datetime.timedelta(seconds=7999))
        assert candles_array.time(-1) == \
            time_to_secs(datetime.datetime(2010, 1, 1))

    # TODO pendiente completar los tests de CandlesArray (almenos el rango es correcto)
    def test_open(self, empty_candles_array: CandlesArray, g_historical_data):
        candles_array = self.simulated_candles_array(empty_candles_array, g_historical_data)

    def test_high(self, empty_candles_array: CandlesArray, g_historical_data):
        candles_array = self.simulated_candles_array(empty_candles_array, g_historical_data)

    def test_low(self, empty_candles_array: CandlesArray, g_historical_data):
        candles_array = self.simulated_candles_array(empty_candles_array, g_historical_data)

    def test_close(self, empty_candles_array: CandlesArray, g_historical_data):
        candles_array = self.simulated_candles_array(empty_candles_array, g_historical_data)


class TestRequestsQueue:
    @pytest.fixture()
    def req_queue(self):
        req_queue = RequestsQueue()
        req_queue.add(1, "e1", "t1", lambda: "a1")
        req_queue.add(1, "e2", "t2", lambda: "a2")
        req_queue.add(1, "e3", "t3", lambda: "a3")
        req_queue.add(2, "e1", "t1", lambda: "a1")
        req_queue.add(1, "e4", "t3", lambda: "a4")
        return req_queue

    def test_add(self, req_queue):
        req_queue.q = req_queue[:3]
        assert len(req_queue) == 3
        assert req_queue.first.valid_id == 1
        assert req_queue.first.emitter == "e1"
        assert req_queue.first.target == "t1"
        assert req_queue.first.action() == "a1"
        assert len(req_queue) == 3
        assert req_queue.last.valid_id == 1
        assert req_queue.last.emitter == "e3"
        assert req_queue.last.target == "t3"
        assert req_queue.last.action() == "a3"
        # asegurar que first no cambió con la adición de un nuevo futuro

    def test_find(self, req_queue):
        for index, future in enumerate(req_queue.find(emitter="e1")):
            assert future == Future(index + 1, "e1", "t1", lambda: "a1")
        test_futures =\
            [Future(1, "e1", "t1", lambda: "a1"),
             Future(1, "e2", "t2", lambda: "a2"),
             Future(1, "e3", "t3", lambda: "a3"),
             Future(1, "e4", "t3", lambda: "a4")]
        for i, future in enumerate(req_queue.find(valid_id=1)):
            assert future == test_futures[i]

        assert req_queue.find(emitter="e2", get_indexes=True) == \
            [(1, Future(1, "e2", "t2", lambda: "a2"))]

        futures = req_queue.find(emitter="e1", get_indexes=True)
        assert futures[0] == (0, Future(1, "e1", "t1", lambda: "a1"))
        assert futures[1] == (3, Future(2, "e1", "t1", lambda: "a1"))

    def test_process(self, req_queue: RequestsQueue):
        assert len(req_queue) == 5
        assert req_queue.process(valid_id=1, target="t3") == \
            Future(1, "e3", "t3", lambda: "a3")
        assert len(req_queue) == 4
        assert req_queue.process(valid_id=1) == \
            Future(1, "e1", "t1", lambda: "a1")
        assert len(req_queue) == 3

        assert req_queue.process(valid_id=1, target="t2").action() == "a2"
        assert len(req_queue) == 2
        assert req_queue.process(valid_id=1, target="t2") is None

    def test_empty_queue(self):
        req_queue = RequestsQueue()
        assert req_queue.process(valid_id=1) is None


class TestRequest:
    @pytest.fixture()
    def IbMock(self):
        class IbMock:
            def __init__(self, valid_id):
                self.valid_id = valid_id

            @request
            def request(self, val):
                return val

        return IbMock

    def test_id_increment(self, IbMock):
        ibmock = IbMock(valid_id=1)
        assert ibmock.request(4) == 4
        ibmock.request(None)
        assert ibmock.valid_id == 2


class TestResponse:
    @pytest.fixture
    def ibmock(self):
        class IbMock: 
            req_queue = RequestsQueue()
            req_queue.add(1, "emitter", "func", 
                          lambda: True)
            
            @response
            def func(self, arg):
                return arg
        
        return IbMock()

    def test_removes_item_from_queue(self, ibmock):
        assert ibmock.func(12) == 12
        assert req_queue


def test_to_datetime():
    test_date = datetime.datetime(
        2000, 1, 1, 10, 10, 10
    )

    assert to_datetime("20000101 10:10:10") == test_date
    assert to_datetime(946735810) == test_date
    assert to_datetime(test_date) == test_date
