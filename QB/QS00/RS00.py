import os
import sys
import time

from data.Function import test_run, start_application
from data.config import programs, WeChat
from data.wechatStart import find_wechat_process, connect_to_wechat_window, focus_wechat_window, send_enter_to_wechat

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
    for app_path in WeChat:
        start_application(app_path)
        time.sleep(1)

    if focus_wechat_window():
        print("锁定窗口")
        if send_enter_to_wechat():
            print("回车登录")

