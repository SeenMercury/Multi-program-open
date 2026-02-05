import os
import sys
import time
import psutil
import win32gui
import win32con
import subprocess
import win32process
import pyautogui as pgui

# ===================================================================================================
# 检测程序是否运行
# ===================================================================================================
def is_program_running(program_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == program_name:
            return True
    return False

# ===================================================================================================
# 查找进程可见窗口
# ===================================================================================================
def find_visible_windows(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                hwnds.append(hwnd)
        return True

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

# ===================================================================================================
# 模拟点击关闭按钮
# ===================================================================================================
def close_window_gracefully(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    start_time = time.time()
    while time.time() - start_time < 1:
        if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
            return True
        time.sleep(0.1)
    return False

# ===================================================================================================
# 启动应用
# ===================================================================================================
def start_application(app_path):
    try:
        # 使用 subprocess.Popen 启动应用程序
        subprocess.Popen(app_path)
        print(f"已启动应用程序: {os.path.basename(app_path)}")
        return True
    except Exception as e:
        print(f"启动应用程序失败: {app_path}\n错误信息: {str(e)}")
        return False

# ====================================================================================================
# ====================================================================================================