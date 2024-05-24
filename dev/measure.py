import sys
sys.path.append("/home/pi/Documents/flexure_exp_proj/src")
from ADXL362 import ADXL362
import time
import concurrent.futures
import functools
import numpy as np
import spidev
# from ADXL362 import ADXL362


def measure(accel, duration=10, increment=0.001)->np.ndarray:
    n_take = int(duration // increment)
    res = np.zeros((n_take, 4))
    counter = 0
    target_time = time.time() + increment
    while counter < n_take:
        if time.time() < target_time:
            continue
        else:
            res[counter] = accel.read_txyz()
            counter += 1
            target_time += increment
    res[:, 0] -= res[0, 0] # shift time to start at 0
    return res


# def measure_one(inc, r_time, accel_meas):
#     while time.time() < r_time + inc: pass
#     return accel_meas.read_txyz

# def measure(accel, duration=10, increment=0.001)->np.ndarray:
#     n_take = int(duration // increment)
#     res = np.zeros((n_take, 4))
#     ind = np.arange(n_take, dtype=int)
#     inc_arr = (ind + 1) * increment
#     ref_time = time.time() + 0.1
#     with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
#         worker = functools.partial(measure_one, r_time=ref_time, accel_meas=accel)
#         for i, txyx in zip(ind, executor.map(worker, inc_arr)):
#             res[i] = txyx
#     res[:, 0] -= res[0, 0] # shift time to start at 0
#     return res


if __name__ == "__main__":
    accel = ADXL362()
    accel.begin_measure()
    res = measure(accel, duration=1, increment=1e-3)
    np.save("test_measure_2.npy", res)