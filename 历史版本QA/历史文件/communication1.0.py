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

programs = ["Weixin.exe", "DingTalk.exe", "QQ.exe"]
if all(is_program_running(program) for program in programs):
    os.system('taskkill /IM QQ.exe /F')
    os.system('taskkill /IM DingTalk.exe /F')
    os.system('taskkill /IM Weixin.exe /F')
    sys.exit() #后面改成关闭所有应用
else:
    start_application('D:\\Communication\\Weixin\\Weixin.exe')

    circulate = 0
    while circulate <= 50:
        try:
            login = pgui.locateOnScreen('WeChat.png')
        except Exception as wc:
            print(f"Error locating '微信登录': {wc}")
            circulate = circulate + 1
            continue
        circulate = 51
        pgui.click(login)
        start_application('D:\\Communication\\DingDing\\DingtalkLauncher.exe')
        start_application('D:\\Communication\\QQ\\QQ.exe')

    circulate = 0
    while circulate <= 50:
        start_application('D:\\Communication\\WeChat\\Weixin.exe')
        time.sleep(0.25)
        try:
            login = pgui.locateOnScreen('QQ.png')
        except Exception as wc:
            print(f"Error locating 'QQ登录完毕': {wc}")
            circulate = circulate + 1
            continue
        circulate = 51
        time.sleep(2)

        os.system('taskkill /IM QQ.exe')
        os.system('taskkill /IM Weixin.exe')
        time.sleep(2)
        os.system('taskkill /IM DingTalk.exe')
        # pyinstaller -F -w --add-data "WeChat.png;." --add-data "QQ.png;." 通讯\通讯1.0.py
