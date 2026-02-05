import os
import sys
import time

from Function import test_run, window_inquiry, close_window, start_application
from config import apps, WeChat, programs, time0, time1
# ===================================================================================================
# 副程序，关程序部分
# ===================================================================================================
if all(test_run(program) for program in programs):
    for program in programs:
        print("副程序中")
        os.system(f'taskkill /IM {program} /F')
    print("功能完成")
    time.sleep(3)
    sys.exit()