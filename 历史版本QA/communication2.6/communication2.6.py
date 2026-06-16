import os
import sys
import time
import psutil
import win32gui

from config import apps, WeChat, programs, time0, time1
from defs import is_program_running, find_visible_windows, close_window_gracefully, start_application
from wechatStart import focus_wechat_window, send_enter_to_wechat
# ===================================================================================================
# 关闭
# ===================================================================================================
if all(is_program_running(program) for program in programs):
    for program in programs:
        print("副程序中")
        os.system(f'taskkill /IM {program} /F')
    print("功能完成")
    time.sleep(3)
    sys.exit()
# ===================================================================================================
# 启动
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
                    windows = find_visible_windows(pid)
                    if not windows:
                        continue

                    # 关闭所有可见窗口
                    for hwnd in windows:
                        window_title = win32gui.GetWindowText(hwnd)

                        if close_window_gracefully(hwnd):
                            print("执行中")
                        else:
                            print("执行中")
                            win32gui.PostMessage(hwnd, 0)

            if not found:
                print(f"{program} 未运行")

        print("功能完成")
        time.sleep(3)
        sys.exit()