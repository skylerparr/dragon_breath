from dragon_breath.process import *
import threading
import time

class Kernel(object):
    _process_map = {}
    kernel = None

    def __init__(self):
        pass

    @classmethod
    def spawn(cls, fun):
        if(cls.kernel is None):
            cls.kernel = Kernel()
        p = Process(cls.kernel)
        t = threading.Thread(target=p.spawn, args={fun})
        t.start()
        pid = Pid()
        Kernel._process_map[pid] = p
        return pid

    @classmethod
    def await(self, pid, timeout = None):
        process = Kernel._process_map[pid]
        if(process.is_alive()):
            t = process._get_thread()
            if(timeout is None):
                t.join()
                return process._get_value()
            else:
                t.join(timeout)
                if(t.is_alive()):
                    process.kill()
                    return None
                return process._get_value()
        else:
            return process._get_value()
            

class Process:

    def __init__(self, kernel):
        self._kernel = kernel

    def spawn(self, fun):
        self._thread = threading.current_thread()
        self._value = None
        self._value = fun()

    def is_alive(self):
        return self._get_thread().is_alive()

    def get_kernel(self):
        return self._kernel

    @property
    def pid(self):
        return self._pid
    
    def _get_value(self):
        return self._value

    def _get_thread(self):
        return self._thread

    def kill(self):
        raise RuntimeError

class ProcessTimeoutException:
    pass

class Pid:
    __PID__ = 0

    def __init__(self): 
        Pid.__PID__ = Pid.__PID__ + 1
        self.pid = Pid.__PID__
