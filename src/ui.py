#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图形用户界面模块

这个模块负责实现Linux远程控制客户端的图形界面，主要功能包括：
1. 创建和管理主窗口
2. 提供连接设置界面
3. 实现命令输入和输出显示
4. 处理用户交互事件

主要组件：
- RemoteControlUI类：主界面类，实现所有GUI相关功能

使用示例：
    root = tk.Tk()
    ui = RemoteControlUI(
        root,
        on_connect=handle_connect,
        on_disconnect=handle_disconnect,
        on_send_command=handle_command
    )
    root.mainloop()

依赖：
- tkinter：Python标准GUI库

作者：Cursor Team
版本：0.1.0
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging

class RemoteControlUI:
    """Linux远程控制客户端图形界面类
    
    实现了完整的图形用户界面，包括连接设置、命令输入输出等功能。
    使用回调函数处理用户操作，支持自定义事件处理。
    
    属性：
        root: Tkinter主窗口实例
        logger: 日志记录器实例
    """
    
    def __init__(self, root, on_connect, on_disconnect, on_send_command):
        """初始化图形界面
        
        Args:
            root: Tkinter主窗口实例
            on_connect: 连接按钮回调函数
            on_disconnect: 断开连接回调函数
            on_send_command: 发送命令回调函数
        """
        self.logger = logging.getLogger('LinuxRemoteControl.UI')
        self.root = root
        self.root.title('Linux远程控制客户端')
        self.root.geometry('800x600')
        self.logger.info('初始化图形界面')

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

        # 连接状态标签
        self.status_label = ttk.Label(self.connection_frame, text='未连接', foreground='red')
        self.status_label.grid(row=0, column=7, padx=5)

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
            self.status_label.config(text='正在连接...', foreground='orange')
            connection_info = {
                'ip': self.ip_entry.get(),
                'username': self.username_entry.get(),
                'password': self.password_entry.get()
            }
            try:
                if self.on_connect(connection_info):
                    self.connect_btn.config(text='断开')
                    self.status_label.config(text='已连接', foreground='green')
            except Exception as e:
                self.status_label.config(text='连接失败', foreground='red')
                self.show_error('连接错误', str(e))
        elif self.connect_btn['text'] == '断开':
            self.on_disconnect()
            self.connect_btn.config(text='连接')
            self.status_label.config(text='未连接', foreground='red')

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