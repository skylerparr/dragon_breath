import unittest
import pytest
import time
import math

from dragon_breath.kernel import *

class TestKernel(unittest.TestCase):

    def return_value(self):
        return "bacon"

    def setUp(self):
        MockWorker.breakout = False

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
            Kernel.await(p, 0.05)
            assert True == False
        except RuntimeError:
            assert True == True
        finally:
            MockWorker.breakout = True

    def test_should_pass_args_to_function(self):
        p = Kernel.spawn(MockWorker().run_with_args, [10])
        value = Kernel.await(p, 1)
        assert 10240 == value
        MockWorker.breakout = True

    def test_should_not_await_if_the_value_is_ready(self):
        p = Kernel.spawn(self.return_value)
        assert "bacon" == Kernel.await(p, 1)
        MockWorker.breakout = True

class MockWorker:
    breakout = False

    def do_lots_of_work(self):
        x = 0
        while(x < 5):
            time.sleep(.01)
            x = x + 1
        return "eggs"

    def run_forever(self):
        while 1 == 1:
            if(MockWorker.breakout):
                break

    def run_with_args(self, y):
        x = 0
        count = y
        while(x < count):
            if(MockWorker.breakout):
                break
            time.sleep(.01)
            x = x + 1
            y = y + y
        return y
