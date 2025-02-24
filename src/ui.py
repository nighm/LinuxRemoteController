import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class RemoteControlUI:
    def __init__(self, root, on_connect, on_disconnect, on_send_command):
        self.root = root
        self.root.title('Linux远程控制客户端')
        self.root.geometry('800x600')

        # 回调函数
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_send_command = on_send_command

        self._init_connection_frame()
        self._init_terminal_frame()

    def _init_connection_frame(self):
        self.connection_frame = ttk.LabelFrame(self.root, text='连接设置', padding='10')
        self.connection_frame.pack(fill='x', padx=10, pady=5)

        # IP地址输入
        ttk.Label(self.connection_frame, text='IP地址:').grid(row=0, column=0, padx=5)
        self.ip_entry = ttk.Entry(self.connection_frame)
        self.ip_entry.grid(row=0, column=1, padx=5)

        # 用户名输入
        ttk.Label(self.connection_frame, text='用户名:').grid(row=0, column=2, padx=5)
        self.username_entry = ttk.Entry(self.connection_frame)
        self.username_entry.grid(row=0, column=3, padx=5)

        # 密码输入
        ttk.Label(self.connection_frame, text='密码:').grid(row=0, column=4, padx=5)
        self.password_entry = ttk.Entry(self.connection_frame, show='*')
        self.password_entry.grid(row=0, column=5, padx=5)

        # 连接按钮
        self.connect_btn = ttk.Button(self.connection_frame, text='连接', command=self._handle_connect)
        self.connect_btn.grid(row=0, column=6, padx=5)

    def _init_terminal_frame(self):
        self.terminal_frame = ttk.LabelFrame(self.root, text='终端', padding='10')
        self.terminal_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 输出文本框
        self.output_text = tk.Text(self.terminal_frame, wrap=tk.WORD, height=20)
        self.output_text.pack(fill='both', expand=True)

        # 命令输入框架
        self.command_frame = ttk.Frame(self.terminal_frame)
        self.command_frame.pack(fill='x', pady=5)

        # 命令输入
        self.command_entry = ttk.Entry(self.command_frame)
        self.command_entry.pack(side='left', fill='x', expand=True)

        # 发送按钮
        self.send_btn = ttk.Button(self.command_frame, text='发送', command=self._handle_send_command)
        self.send_btn.pack(side='right', padx=5)

    def _handle_connect(self):
        if self.connect_btn['text'] == '连接':
            connection_info = {
                'ip': self.ip_entry.get(),
                'username': self.username_entry.get(),
                'password': self.password_entry.get()
            }
            if self.on_connect(connection_info):
                self.connect_btn.config(text='断开')
        else:
            self.on_disconnect()
            self.connect_btn.config(text='连接')

    def _handle_send_command(self):
        command = self.command_entry.get()
        if command:
            self.on_send_command(command)
            self.command_entry.delete(0, 'end')

    def append_output(self, text):
        self.output_text.insert('end', text)
        self.output_text.see('end')

    def show_error(self, title, message):
        messagebox.showerror(title, message)