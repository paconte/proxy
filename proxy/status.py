"""Status class of the proxy

The status class is designed to be multithread.
"""
import datetime
import time
from multiprocessing import Value, Lock


class Status():
    """The class counter must work with multithreads"""
    start = time.time()
    counter = Value('i', 0)
    lock = Lock()

    @classmethod
    def increment(cls):
        """increments the proxy requests by one."""
        with cls.lock:
            cls.counter.value += 1

    @classmethod
    def requests(cls):
        """returns the current total requests"""
        with cls.lock:
            return cls.counter.value

    @classmethod
    def running(cls):
        """
        returns the total number of seconds the proxy
        is running since it starts.
        """
        return time.time() - cls.start

    @classmethod
    def running_str(cls):
        """returns the total running time in a human readable from."""
        return datetime.timedelta(seconds=cls.running())
