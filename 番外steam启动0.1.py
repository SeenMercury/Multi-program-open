import ctypes
import os
import subprocess


def start_application(app_path, require_admin=False):
    """启动指定的应用程序"""
    try:
        if require_admin:
            # 使用 ShellExecute 以管理员权限启动应用程序，这会触发UAC提示
            result = ctypes.windll.shell32.ShellExecuteW(
                None,  # 父窗口句柄
                "runas",  # 操作 - 请求管理员权限
                app_path,  # 要执行的应用程序
                None,  # 参数
                None,  # 工作目录
                1  # 显示窗口 (SW_SHOWNORMAL)
            )

            # ShellExecute 返回大于32的值表示成功
            if result <= 32:
                print(f"启动应用程序失败: {os.path.basename(app_path)} (错误代码: {result})")
                return False
            else:
                print(f"已请求启动应用程序: {os.path.basename(app_path)} (等待UAC确认)")
                return True
        else:
            # 使用 subprocess.Popen 启动不需要管理员权限的应用程序
            subprocess.Popen(app_path)
            print(f"已启动应用程序: {os.path.basename(app_path)}")
            return True
    except Exception as e:
        print(f"启动应用程序失败: {app_path}\n错误信息: {str(e)}")
        return False


# 定义应用程序路径列表，标记哪些需要管理员权限
apps = [
    # ('E:/Game/steam/Steam.exe', False),  # Steam不需要管理员权限
    ('E:/Accelerator/AccUpdater/CMCCAcc/client/GameAcc.exe', True),  # 需要管理员权限
    ('E:/Accelerator/Watt Toolkit/Steam++/Steam++.exe', True)  # 需要管理员权限
]

print("开始启动应用程序...")

# 遍历并启动所有应用程序
for app_path, require_admin in apps:
    start_application(app_path, require_admin)

print("\n所有启动请求已完成。")
print("注意：需要管理员权限的应用程序将会显示UAC提示，请根据需要允许或拒绝。")