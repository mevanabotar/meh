
import timeit
import contextlib
import ctypes
from ctypes import wintypes

winmm = ctypes.WinDLL('winmm')

class TIMECAPS(ctypes.Structure):
    _fields_ = (('wPeriodMin', wintypes.UINT),
                ('wPeriodMax', wintypes.UINT))

def _check_time_err(err, func, args):
    if err:
        raise WindowsError('%s error %d' % (func.__name__, err))
    return args

winmm.timeGetDevCaps.errcheck = _check_time_err
winmm.timeBeginPeriod.errcheck = _check_time_err
winmm.timeEndPeriod.errcheck = _check_time_err

@contextlib.contextmanager
def timer_resolution(msecs=0):
    caps = TIMECAPS()
    winmm.timeGetDevCaps(ctypes.byref(caps), ctypes.sizeof(caps))
    msecs = min(max(msecs, caps.wPeriodMin), caps.wPeriodMax)
    winmm.timeBeginPeriod(msecs)
    yield
    winmm.timeEndPeriod(msecs)

def min_sleep():
    setup = 'import time'
    stmt = 'time.sleep(0.001)'
    return timeit.timeit(stmt, setup, number=1000)

#Pg examples
"""
min_sleep()
with timer_resolution(msec=1): min_sleep()
min_sleep()
"""

#Pf references
"""
https://stackoverflow.com/questions/38487114/python-2-x-sleep-call-at-millisecond-level-on-windows
"""
