import os
import sys
import time
import ctypes
import psutil
import win32gui
import win32con
import subprocess
import win32process
import pyautogui as pgui

#打开程序
def start_application(path):
    try:
        subprocess.Popen(path, shell=True)
    except Exception as e:
        print(f"Error starting application: {e}")

#检测程序是否在运行
def is_program_running(program_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == program_name:
            return True
    return False

def require_admin():
    if os.name == 'nt' and not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, None, 1)
        sys.exit()

# 查找指定进程的所有可见窗口
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

# 优雅关闭窗口（模拟点击关闭按钮）
def close_window_gracefully(hwnd):
    # 发送关闭消息（WM_CLOSE）
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    # 等待窗口关闭（最多等待1秒）
    start_time = time.time()
    while time.time() - start_time < 1:
        if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
            return True
        time.sleep(0.1)
    return False

programs = ["WeChat.exe", "DingTalk.exe", "QQ.exe", "mailmaster.exe"]
if all(is_program_running(program) for program in programs):
    os.system('taskkill /IM QQ.exe /F')
    os.system('taskkill /IM DingTalk.exe /F')
    os.system('taskkill /IM WeChat.exe /F')
    os.system('taskkill /IM mailmaster.exe /F')
    sys.exit() # 程序退出模块
else:
    start_application('D:\\Communication\\Weixin\\WeChat\\WeChat.exe')

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
        start_application('D:/Communication/DingDing/DingtalkLauncher.exe')
        start_application('D:/Communication/QQ/QQ.exe')
        start_application('D:/Communication/.com/MailMaster/Application/mailmaster.exe')
        time.sleep(10) #程序启动

    if __name__ == "__main__":
        require_admin()  # 请求管理员权限

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

        print("所有程序处理完成")
        print("提示：这些程序可能仍在后台运行（系统托盘）")