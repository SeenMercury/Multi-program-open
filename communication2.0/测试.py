# 在主文件中
import os
import time


from 测试1 import focus_wechat_window, send_enter_to_wechat
import subprocess

def start_application(app_path):
    try:
        # 使用 subprocess.Popen 启动应用程序
        subprocess.Popen(app_path)
        print(f"已启动应用程序: {os.path.basename(app_path)}")
        return True
    except Exception as e:
        print(f"启动应用程序失败: {app_path}\n错误信息: {str(e)}")
        return False

WeChat = [
    'D:/Communication/Weixin/Weixin/Weixin.exe'
]



# 启动微信
for app_path in WeChat:
    start_application(app_path)

# 等待微信启动
time.sleep(2)

# 锁定微信窗口并发送回车
if focus_wechat_window():
    print("成功锁定微信窗口")
    if send_enter_to_wechat():
        print("微信登录成功")
        # 启动其他应用
        for app_path in apps:
            start_application(app_path)
        time.sleep(17)
    else:
        print("微信登录失败")
else:
    print("无法锁定微信窗口")