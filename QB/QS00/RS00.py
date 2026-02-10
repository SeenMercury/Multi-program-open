import os
import sys
import time
import psutil
import win32gui

from data.Function import test_run, start_application, window_inquiry, close_window
from data.config import programs, WeChat, apps, time0, time1
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
    print("主程序中")
    for app_path in WeChat:
        start_application(app_path)

    time.sleep(time1)

    if focus_wechat_window():
        print("锁定微信窗口")
        if send_enter_to_wechat():
            print("微信登录成功")
            # 启动其他应用
            for app_path in apps:
                start_application(app_path)
            time.sleep(time0)
        for program in programs:
            print(f"正在处理 {program}...")
            found = False

            # 查找所有匹配的进程
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == program.lower():
                    pid = proc.info['pid']
                    found = True

                    # 查找进程的所有可见窗口
                    windows = window_inquiry(pid)
                    if not windows:
                        continue

                    # 关闭所有可见窗口
                    for hwnd in windows:
                        window_title = win32gui.GetWindowText(hwnd)

                        if close_window(hwnd):
                            print("执行中")
                        else:
                            print("执行中")
                            win32gui.PostMessage(hwnd, 0)

            if not found:
                print(f"{program} 未运行")

        print("功能完成")
        time.sleep(3)
        sys.exit()