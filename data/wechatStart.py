import time
import psutil
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError


def find_wechat_process():
    for proc in psutil.process_iter(['pid', 'name']):
        # 微信进程名可能是WeChat.exe或Weixin.exe
        if proc.info['name'].lower() in ['wechat.exe', 'weixin.exe']:
            print(f"找到微信进程: PID {proc.info['pid']}")
            return proc.info['pid']
    print("未找到微信进程")
    return None


def connect_to_wechat_window(timeout=30):
    start_time = time.time()

    # 等待微信进程启动
    wechat_pid = None
    while time.time() - start_time < timeout and wechat_pid is None:
        wechat_pid = find_wechat_process()
        if wechat_pid is None:
            time.sleep(1)

    if wechat_pid is None:
        print("等待微信进程启动超时")
        return None, None

    # 尝试通过进程ID连接
    try:
        app = Application().connect(process=wechat_pid)
        print(f"通过进程ID {wechat_pid} 连接到微信")
        return app, app.window(title_re=".*微信.*")
    except ElementNotFoundError:
        print("通过进程ID连接失败，尝试通过窗口标题连接")

    # 如果通过进程ID连接失败，尝试通过窗口标题连接
    try:
        app = Application().connect(title_re=".*微信.*", timeout=10)
        main_window = app.window(title_re=".*微信.*")
        print("通过窗口标题连接到微信")
        return app, main_window
    except ElementNotFoundError as e:
        print(f"连接微信窗口失败: {e}")
        return None, None


def focus_wechat_window():
    app, main_window = connect_to_wechat_window()
    if main_window is None:
        return False

    try:
        # 将窗口置于前台
        main_window.set_focus()
        print("微信窗口已聚焦")
        return True
    except Exception as e:
        print(f"聚焦微信窗口失败: {e}")
        return False


def send_enter_to_wechat():
    if not focus_wechat_window():
        return False

    time.sleep(0.5)

    # 可以直接发送回车键
    try:
        import pyautogui
        pyautogui.press('enter')
        print("已发送回车键")
        return True
    except Exception as e:
        print(f"发送回车键失败: {e}")
        return False