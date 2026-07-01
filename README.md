# 应用多开器

一个轻量级的自动化脚本，用于批量启动和管理多个应用程序。它会自动检测指定软件是否已运行，若未启动则执行启动；同时可以根据配置自动关闭某些窗口，适用于需要同时存在多个相同类型应用的场景。

## 功能特点

- 自动检测指定程序是否已运行
- 批量启动多个应用
- 可配置哪些应用启动后需要自动关闭窗口
- 支持设置启动后的等待时间，避免程序启动过快导致操作失败

## 环境要求

- Windows 操作系统
- Python 3.x

安装依赖：

```bash
pip install -r requirements.txt
```

## 配置说明

在使用前，需要先配置对应版本目录下的 config.py 文件。常见配置项如下：

```python
apps = [
    r"C:\Program Files\YourApp\app.exe",
    r"C:\Program Files\YourApp\app2.exe"
]

programs0 = ["app.exe", "app2.exe"]

programs1 = ["app.exe"]

time0 = 17
```

参数说明：

- apps：要启动的应用程序完整路径
- programs0：需要检查的程序文件名或进程名
- programs1：启动后希望默认关闭窗口的应用
- time0：应用启动后等待关闭窗口的时间，单位为秒，默认建议为 17

## 运行方式

配置完成后，运行对应版本的主程序即可：

```bash
python communication.py
```

如果你使用的是某个特定版本目录（例如 communication2.4 或 communication2.5），请进入对应目录后再运行相应脚本。

## 运行示例

```text
已启动应用程序: DingtalkLauncher.exe
已启动应用程序: QQ.exe
已启动应用程序: mailmaster.exe
正在处理 DingTalk.exe...
执行中
功能完成
```

## 注意事项

- 路径建议使用原始字符串形式，避免转义字符导致异常
- 某些程序启动后可能需要更长时间才会完全初始化，适当调整 time0 的值
- 如需修改程序名或关闭逻辑，请同步更新 config.py 中的配置
