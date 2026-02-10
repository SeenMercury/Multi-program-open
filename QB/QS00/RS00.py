import os
import sys
import time

from data.Function import test_run
from data.config import programs

# ===================================================================================================
# 分类 有活干活 没活散伙 运行0
# ===================================================================================================
any_running = any(test_run(program_name) for program_name in programs)
if any_running:
    for program_name in programs:
        print("运行0")
        os.system(f'taskkill /IM {program_name} /F')

    print("程序完成")
    time.sleep(3)
    sys.exit()
# ===================================================================================================
# 运行1
# ===================================================================================================
else:
    print("运行1")
