import os
import subprocess


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
    'E:/Game/steam/Steam.exe',
    'E:/Accelerator/AccUpdater/CMCCAcc/client/GameAcc.exe',
    'E:/Accelerator/Watt Toolkit/Steam++/Steam++.exe'
]
# ===================================================================================================
for app in apps:
    start_application(app)