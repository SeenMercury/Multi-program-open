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
# 打开程序
# ===================================================================================================
def start_application(path):
    try:
        subprocess.Popen(path, shell=True)
    except Exception as e:
        print(f"Error starting application: {e}")

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
# 定义应用
# ===================================================================================================
def start_application(app_path):
    """启动指定的应用程序"""
    try:
        # 使用 subprocess.Popen 启动应用程序
        subprocess.Popen(app_path)
        print(f"已启动应用程序: {os.path.basename(app_path)}")
        return True
    except Exception as e:
        print(f"启动应用程序失败: {app_path}\n错误信息: {str(e)}")
        return False

# 定义应用程序路径列表
apps = [
    'D:/Communication/DingDing/DingtalkLauncher.exe',
    'D:/Communication/QQ/QQ.exe',
    'D:/Communication/.com/MailMaster/Application/mailmaster.exe'
]
WeChat = [
    'D:/Communication/Weixin/WeChat/WeChat.exe'
]
# ===================================================================================================
# 关闭
# ===================================================================================================
programs = ["WeChat.exe", "DingTalk.exe", "QQ.exe", "mailmaster.exe"]

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

    Mercury = 0
    while Mercury <= 50:
        try:
            login = pgui.locateOnScreen('WeChat.png')
        except Exception as wc:
            print(f"Error locating WeChat: {wc}")
            Mercury = Mercury + 1
            continue
        Mercury = 51
        pgui.click(login)
        for app_path in apps:
            start_application(app_path)
        time.sleep(12)

    if __name__ == "__main__":

        programs = ["QQ.exe", "WeChat.exe", "DingTalk.exe", "mailmaster.exe"]

        for program in programs:
            print(f"正在处理 {program}...")
            found = False

            # 查找所有匹配的进程
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == program.lower():
                    pid = proc.info['pid']
                    found = True
                    print(f"找到进程: {program} (PID: {pid})")

                    # 查找进程的所有可见窗口
                    windows = find_visible_windows(pid)
                    if not windows:
                        print(f"  - {program} 没有可见窗口（已后台运行）")
                        continue

                    # 关闭所有可见窗口
                    for hwnd in windows:
                        window_title = win32gui.GetWindowText(hwnd)
                        print(f"  - 关闭窗口: {window_title}")

                        if close_window_gracefully(hwnd):
                            print("    ✓ 窗口已关闭")
                        else:
                            print("    ⚠ 无法关闭窗口，尝试强制关闭")
                            win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_CLOSE, 0)

            if not found:
                print(f"{program} 未运行")

            print("")
        print("功能完成")