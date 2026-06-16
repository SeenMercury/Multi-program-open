import tkinter as tk
import ast
import os
import sys

from tkinter import ttk, messagebox, scrolledtext

class ConfigEditor:
    def __init__(self, master):

# ===================================================================================================
# 窗口配置
# ===================================================================================================
        self.master = master
        self.master.title("配置文件编辑器")
        self.master.geometry("700x600")

# ===================================================================================================
# 配置文件路径
# ===================================================================================================
        self.config_file = "config.py"

# ===================================================================================================
# 初始化实例
# ===================================================================================================
        self.config_data = None
        self.apps_frame = None
        self.wechat_frame = None
        self.programs_frame = None
        self.time_frame = None
        self.apps_text = None
        self.wechat_text = None
        self.programs_text = None
        self.time0_var = None
        self.time1_var = None
        self.time0_entry = None
        self.time1_entry = None

# ===================================================================================================
# 加载配置
# ===================================================================================================
        self.config_data = self.load_config()
        if self.config_data is None:
            messagebox.showerror("错误", f"无法加载配置文件 {self.config_file}")
            sys.exit(1)

        # 创建界面
        self.create_widgets()

        # 填充数据
        self.populate_data()

    def load_config(self):
        """加载配置文件并解析内容"""
        if not os.path.exists(self.config_file):
            return None

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析Python代码
            parsed = ast.parse(content)

            config_data = {}
            for node in parsed.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            # 获取变量的值
                            if isinstance(node.value, ast.List):
                                # 处理列表
                                values = []
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                        values.append(elt.value)
                                config_data[var_name] = values
                            elif isinstance(node.value, ast.Constant):
                                # 处理常量（数字、字符串等）
                                config_data[var_name] = node.value.value
            return config_data
        except Exception as e:
            print(f"解析配置文件时出错: {e}")
            return None

    def create_widgets(self):
        """创建界面组件"""
        # 创标签页
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # 标签页0
        self.apps_frame = ttk.Frame(notebook)
        notebook.add(self.apps_frame, text="需开启的应用路径")

        # 标签页1
        self.wechat_frame = ttk.Frame(notebook)
        notebook.add(self.wechat_frame, text="微信路径")

        # 标签页2
        self.programs_frame = ttk.Frame(notebook)
        notebook.add(self.programs_frame, text="需关闭的程序列表")

        # 标签页3
        self.time_frame = ttk.Frame(notebook)
        notebook.add(self.time_frame, text="定时设置")

        # 创建各个标签页的内容
        self.create_apps_tab()
        self.create_wechat_tab()
        self.create_programs_tab()
        self.create_time_tab()

        # 保存按钮
        save_button = ttk.Button(self.master, text="保存配置", command=self.save_config)
        save_button.pack(pady=10)

    def create_apps_tab(self):
        """创建应用路径标签页"""
        label = ttk.Label(self.apps_frame, text="应用路径列表 (每行一个路径):")
        label.pack(pady=5)

        self.apps_text = scrolledtext.ScrolledText(self.apps_frame, height=10, width=80)
        self.apps_text.pack(padx=10, pady=5, fill='both', expand=True)

    def create_wechat_tab(self):
        """创建微信路径标签页"""
        label = ttk.Label(self.wechat_frame, text="微信路径列表 (每行一个路径):")
        label.pack(pady=5)

        self.wechat_text = scrolledtext.ScrolledText(self.wechat_frame, height=5, width=80)
        self.wechat_text.pack(padx=10, pady=5, fill='both', expand=True)

    def create_programs_tab(self):
        """创建程序列表标签页"""
        label = ttk.Label(self.programs_frame, text="程序列表 (每行一个程序名):")
        label.pack(pady=5)

        self.programs_text = scrolledtext.ScrolledText(self.programs_frame, height=10, width=80)
        self.programs_text.pack(padx=10, pady=5, fill='both', expand=True)

    def create_time_tab(self):
        """创建时间设置标签页"""
        # time0 设置
        time0_frame = ttk.Frame(self.time_frame)
        time0_frame.pack(fill='x', padx=10, pady=10)

        time0_label = ttk.Label(time0_frame, text="time0 值:")
        time0_label.pack(side='left')

        self.time0_var = tk.StringVar()
        self.time0_entry = ttk.Entry(time0_frame, textvariable=self.time0_var, width=10)
        self.time0_entry.pack(side='left', padx=5)

        # time1 设置
        time1_frame = ttk.Frame(self.time_frame)
        time1_frame.pack(fill='x', padx=10, pady=10)

        time1_label = ttk.Label(time1_frame, text="time1 值:")
        time1_label.pack(side='left')

        self.time1_var = tk.StringVar()
        self.time1_entry = ttk.Entry(time1_frame, textvariable=self.time1_var, width=10)
        self.time1_entry.pack(side='left', padx=5)

    def populate_data(self):
        """将配置数据填充到界面"""
        # 填充 apps
        if 'apps' in self.config_data:
            apps_text = '\n'.join(self.config_data['apps'])
            self.apps_text.insert('1.0', apps_text)

        # 填充 WeChat
        if 'WeChat' in self.config_data:
            wechat_text = '\n'.join(self.config_data['WeChat'])
            self.wechat_text.insert('1.0', wechat_text)

        # 填充 programs
        if 'programs' in self.config_data:
            programs_text = '\n'.join(self.config_data['programs'])
            self.programs_text.insert('1.0', programs_text)

        # 填充 time0 和 time1
        if 'time0' in self.config_data:
            self.time0_var.set(str(self.config_data['time0']))
        if 'time1' in self.config_data:
            self.time1_var.set(str(self.config_data['time1']))

    def save_config(self):
        """保存配置到文件"""
        try:
            # 获取界面中的数据
            apps = [line.strip() for line in self.apps_text.get('1.0', tk.END).strip().split('\n') if line.strip()]
            wechat = [line.strip() for line in self.wechat_text.get('1.0', tk.END).strip().split('\n') if line.strip()]
            programs = [line.strip() for line in self.programs_text.get('1.0', tk.END).strip().split('\n') if
                        line.strip()]

            # 验证时间值
            try:
                time0 = int(self.time0_var.get())
                time1 = int(self.time1_var.get())
            except ValueError:
                messagebox.showerror("错误", "时间值必须是整数")
                return

            # 生成配置文件内容
            config_content = f"""apps = {apps}
WeChat = {wechat}
programs = {programs}
time0 = {time0}
time1 = {time1}
"""

            # 写入文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)

            messagebox.showinfo("成功", "配置已保存")

        except Exception as e:
            messagebox.showerror("错误", f"保存配置时出错: {e}")