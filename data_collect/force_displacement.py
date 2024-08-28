import sys
sys.path.append("/Users/andrewliu/Documents/exp_proj/flexure_exp_proj/src")
from TI500E import read_scale_data
from DITR0105 import read_caliper_data
from multiprocessing import Process
import time

def main():
    save_duration = 50
    output_dir = '../data/buckling/'
    annotation = '8in_332_3'
    p1 = Process(
        target=read_scale_data, 
        kwargs={'port':'/dev/tty.usbserial-2130', 'save_duration':save_duration, 'output_file':f'{output_dir}scale_{annotation}.txt'}
    )
    p2 = Process(
        target=read_caliper_data,
        kwargs={'save_duration':save_duration, 'output_file':f'{output_dir}caliper_{annotation}.txt'}
    )
    p2.start()
    time.sleep(1)
    p1.start()


if __name__ == "__main__":
    main()