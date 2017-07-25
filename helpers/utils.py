import time
import datetime
import inspect
import numpy as np


def virtual(fn):
    """
    Decorador.
    Existe para informar que el elemento decorado debe ser
    sobreescrito.
    """
    return fn


def request(original_function):
    def new_function(self, *args, **kwargs):
        assert self.valid_id is not None, \
            "self.valid_id no puede ser None"
        resp = original_function(self, *args, **kwargs)
        if not resp:
            resp = self.valid_id
            self.valid_id += 1
        return resp
    return new_function


def response(original_function):
    def new_function(self, req_id: int, *args, **kwargs):

        def process_queue(q: RequestsQueue):
            q.process(valid_id=req_id, target=original_function.__name__)

        process_queue(self.req_queue)
        return original_function(self, *args, **kwargs)
    return new_function

__historical_data_structure = [('time', '<i4'), ('open', '<f4'), ('high', '<f4'), ('low', '<f4'), ('close', '<f4')]


def historical_data_to_numpy(data: list):
    if len(data) > 0:
        assert (type(data[0]) == tuple), "el elemento interno de data debe ser un " \
                                         "tuple pero es un <%s>" % type(data[0])
        assert(len(data[0]) == 5), "La estructura de la lista no coincide, " \
                                   "la lista interna tiene %s elementos, deberia tener 5" % len(data[0])

    quotes = np.array(
        data,
        dtype=__historical_data_structure)
    return quotes


def time_to_secs(_time_):
    return int(time.mktime(_time_.timetuple()))


class CandlesArray:
    def __init__(self):
        self.req_id = None
        self.data = historical_data_to_numpy([])

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        return np.array_equal(self.data, other.data) and \
               (self.req_id == other.req_id)

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self):
        return self.data

    def add_candle(self, 
                   tick_datetime,
                   open: int,
                   high: int,
                   low: int,
                   close: int):
        if type(tick_datetime) == str:
            datetime_ = datetime.datetime.strptime(tick_datetime, "%Y%m%d %H:%M:%S")
            secs = time_to_secs(datetime_)
        elif type(tick_datetime) == datetime.datetime:
            secs = time_to_secs(tick_datetime)
        elif type(tick_datetime) == int or type(tick_datetime) == np.int32:
            secs = tick_datetime
        else:
            raise TypeError("tick_datetime should be a str, a datetime or an integer but is %s" % type(tick_datetime))

        self.data = np.append(self.data, historical_data_to_numpy([(secs, open, high, low, close)]))

    @staticmethod
    def change_bar_size(data, barsize=datetime.timedelta()):
        newdata = []
        # bardelta es la relacion entre el barsize que se desea y
        # el ancho de la barra de los datos.
        # eg: se desea 1 min, y el ancho de la barra de data es de 1 sec,
        # bardelta seria 60.
        bardelta = barsize.total_seconds() / (data[1]['time'] - data[0]['time'])

        def create_candle(a, b):
            candle = (data[a]['time'],
                      data[a]['open'],
                      np.max(data[a:b]['high']),
                      np.min(data[a:b]['low']),
                      data[b-1]['close'])
            return candle

        j = 0
        for i in range(int(bardelta), len(data), int(bardelta)):
            newdata.append(create_candle(j, i))
            j = i
        newdata.append(create_candle(j, len(data)))
        return historical_data_to_numpy(newdata)

    def get_candles(self, bar_size="seconds"):
        if bar_size:
            return self.data
        if bar_size == "hours":
            # TODO agregar el cambio de bar_size
            for i in self.data:
                pass

    def time(self, index):
        return self.data["time"][-1 - index]

    def open(self, index):
        return self.data["open"][-1 - index]

    def high(self, index):
        return self.data["high"][-1 - index]

    def low(self, index):
        return self.data["low"][-1 - index]

    def close(self, index):
        return self.data["close"][-1 - index]


class Future:
    def __init__(self, valid_id, emitter, target, action):
        self.valid_id = valid_id
        self.emitter = emitter
        self.target = target
        self.action = action

    def __eq__(self, other):
        return (
            self.valid_id == other.valid_id and
            self.emitter == other.emitter and
            self.target == other.target)

    def __repr__(self):
        return "<Future {} > {} > {}>".format(
            self.valid_id, self.emitter, self.target)


class RequestsQueue:

    def __init__(self):
        self.q = []

    def __len__(self):
        return len(self.q)

    def __iter__(self):
        return self.q

    def __getitem__(self, item):
        return self.q[item]

    def add(self, valid_id, emitter, target, action):
        future = Future(
            valid_id, emitter, target, action
        )
        self.q.append(future)

    @property
    def first(self) -> Future:
        return self.q[0]

    @property
    def last(self) -> Future:
        return self.q[-1]

    def find(self, valid_id=None, emitter=None, target=None, get_indexes=False):
        indexes = []

        def request_filter(arg):
            def filt(index, future):
                if valid_id:
                    if future.valid_id != valid_id:
                        return
                if emitter:
                    if future.emitter != emitter:
                        return
                if target:
                    if future.target != target:
                        return
                indexes.append(index)
                return True
            return filt(*arg)
        index_and_future = list(filter(request_filter, list(enumerate(self.q))))

        if get_indexes:
            return index_and_future
        else:
            return [future for index, future in index_and_future]

    def process(self, valid_id=None, emitter=None, target=None) -> Future:
        index_and_future = self.find(valid_id, emitter, target, get_indexes=True)

        try:
            index, future = index_and_future[0]
        except IndexError:
            return None
        else:
            # filter out the future to be processed
            self.q = [f for (i, f) in enumerate(self.q) if i != index]

        return future


format_ = "%Y%m%d %H:%M:%S"


def datetime_to_str(dt: datetime.datetime):
    return dt.strftime(format_)


def str_to_datetime(dt_str: str):
    return datetime.datetime.strptime(dt_str, format_)
