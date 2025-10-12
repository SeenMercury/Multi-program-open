import os
import sys
import time
import psutil
import subprocess
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

    programs = ["QQ.exe", "WeChat.exe", "DingTalk.exe", "mailmaster.exe"]

    for program in programs:
        while True:
            if is_program_running(program):
                print(f"{program} is detected.")
                os.system(f'taskkill /IM {program}')
                print(f"{program} has been terminated.")
                break
            else:
                print(f"{program} is not running.")
            time.sleep(0.5)
            # pyinstaller -F -w 通讯1.1.py
            # pyinstaller -w 通讯1.1.py