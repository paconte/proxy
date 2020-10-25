import unittest
from multiprocessing import Process
import proxy.status as status
from time import sleep


class TestProxyStatus(unittest.TestCase):
    def test_proxy_status(self):
        def func_increment():
            for i in range(100):
                sleep(0.01)
                status.Status.increment()

        procs = [Process(target=func_increment) for i in range(10)]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
        if True:
            print(status.Status.requests())
        self.assertEqual(1000, status.Status.requests())


if __name__ == "__main__":
    unittest.main()
