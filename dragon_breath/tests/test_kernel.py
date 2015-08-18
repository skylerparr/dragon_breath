import unittest
import pytest
import time

from dragon_breath.kernel import *

class TestKernel(unittest.TestCase):

    def return_value(self):
        return "bacon"

    def test_should_only_create_one_kernel(self):
        p1 = Kernel.spawn(self.return_value)
        p2 = Kernel.spawn(self.return_value)
        assert Kernel.kernel == Kernel.kernel
        
    def test_should_get_value_of_function(self):
        p = Kernel.spawn(MockWorker().do_lots_of_work)
        value = Kernel.await(p)
        assert value == "eggs"

    def test_should_get_pid_number(self):
        p1 = Kernel.spawn(self.return_value)
        assert p1.pid > 0
        p2 = Kernel.spawn(self.return_value)
        assert p1.pid < p2.pid

    def test_should_throw_exception_after_timeout(self):
        try:
            p = Kernel.spawn(MockWorker().run_forever)
            Kernel.await(p, 1)
            assert True == False
        except RuntimeError:
            assert True == True
        finally:
            MockWorker.breakout = True

class MockWorker:
    breakout = False

    def do_lots_of_work(self):
        x = 0
        while(x < 5):
            time.sleep(.1)
            x = x + 1
        return "eggs"

    def run_forever(self):
        while 1 == 1:
            if(MockWorker.breakout):
                break
