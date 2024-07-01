import sys
sys.path.append("/home/pi/Documents/flexure_exp_proj/src")
from measure_oscil import measure
import numpy as np
from ADXL362 import ADXL362


if __name__ == "__main__":
    CONFIG_ID = 7
    TAKE_NUM = 3
    AXIS = 'blue'
    accel = ADXL362()
    accel.begin_measure()
    res = measure(accel, duration=5)
    np.save(f"../data/norm_mode_null_test/NullTest_config{CONFIG_ID}-{AXIS}-take{TAKE_NUM}.npy", res)
    # np.save(f"../data/norm_mode_null_test/NullTest_no_hit_take{TAKE_NUM}.npy", res)