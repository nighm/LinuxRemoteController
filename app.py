#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Linux远程控制客户端主程序

这个模块是应用程序的主入口，负责：
1. 初始化日志系统
2. 创建图形界面
3. 管理SSH连接
4. 处理用户交互

主要组件：
- Application类：应用程序的主类，协调UI和SSH连接
- setup_logging函数：配置日志系统

使用方法：
    python app.py

依赖：
- tkinter：GUI库
- paramiko：SSH客户端库
- logging：日志记录

作者：Cursor Team
版本：0.1.0
"""

import tkinter as tk
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from src.ui import RemoteControlUI
from src.ssh import SSHConnection


def setup_logging():
    """配置应用程序的日志系统
    
    创建一个循环日志文件处理器和控制台处理器，实现同时输出到文件和控制台。
    日志文件限制单个大小为1MB，最多保留5个备份文件。
    日志格式包含时间戳、模块名、日志级别和消息。
    
    Returns:
        logging.Logger: 配置好的日志记录器
    
    日志文件位置：./logs/app.log
    日志格式：时间 - 模块名 - 日志级别 - 消息
    """

    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    
    # 配置文件处理器
    log_file = log_dir / 'app.log'
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024 * 5,  # 5MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # 配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    
    # 配置根日志记录器
    logger = logging.getLogger('LinuxRemoteControl')
    logger.setLevel(logging.DEBUG)  # 设置为DEBUG级别以显示所有日志
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # 添加未捕获异常的处理
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.error("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))
    
    import sys
    sys.excepthook = handle_exception
    
    logger.info('日志系统初始化完成')
    logger.debug('日志级别：DEBUG，日志文件路径：%s', log_file)

    return logger

class Application:
    """Linux远程控制客户端应用程序主类
    
    负责协调GUI界面和SSH连接的核心类，管理整个应用程序的生命周期。
    主要功能包括：
    - 初始化和配置日志系统
    - 创建和管理GUI界面
    - 处理SSH连接和断开
    - 执行远程命令并处理结果
    
    属性：
        logger: 日志记录器实例
        root: Tkinter主窗口实例
        ssh: SSH连接管理器实例
        ui: 用户界面实例
    """
    
    def __init__(self):
        """初始化应用程序实例
        
        设置日志记录器并初始化基本组件。所有组件的实际初始化在initialize方法中完成。
        """
        self.logger = setup_logging()
        self.root = None  # Tkinter主窗口
        self.ssh = None   # SSH连接管理器
        self.ui = None    # 用户界面组件
    
    def initialize(self):
        """初始化应用程序组件"""
        try:
            self.root = tk.Tk()
            self.ssh = SSHConnection()
            self.ui = RemoteControlUI(
                self.root,
                on_connect=self._handle_connect,
                on_disconnect=self._handle_disconnect,
                on_send_command=self._handle_send_command
            )
            self.logger.info('应用程序初始化成功')
        except Exception as e:
            self.logger.error(f'应用程序初始化失败: {str(e)}')
            raise
    
    def _handle_connect(self, connection_info):
        try:
            self.ssh.connect(connection_info)
            self.ui.append_output(f'成功连接到 {connection_info["ip"]}\n')
            self.logger.info(f'成功连接到远程主机: {connection_info["ip"]}')
            return True
        except Exception as e:
            error_msg = str(e)
            self.ui.show_error('连接错误', error_msg)
            self.logger.error(f'连接失败: {error_msg}')
            return False
    
    def _handle_disconnect(self):
        try:
            self.ssh.disconnect()
            self.ui.append_output('已断开连接\n')
            self.logger.info('已断开与远程主机的连接')
        except Exception as e:
            self.logger.error(f'断开连接时发生错误: {str(e)}')
    
    def _handle_send_command(self, command):
        try:
            if not self.ssh.is_connected:
                self.ui.show_error('错误', '请先建立连接')
                self.logger.warning('尝试在未连接状态下执行命令')
                return
            
            self.logger.info(f'执行命令: {command}')
            output, error = self.ssh.execute_command(command)
            
            self.ui.append_output(f'\n$ {command}\n')
            if output:
                self.ui.append_output(output)
                self.logger.debug(f'命令输出: {output}')
            if error:
                self.ui.append_output(f'错误: {error}\n')
                self.logger.error(f'命令执行错误: {error}')
        
        except Exception as e:
            error_msg = str(e)
            self.ui.show_error('命令执行错误', error_msg)
            self.logger.error(f'命令执行异常: {error_msg}')
    
    def run(self):
        """运行应用程序"""
        try:
            self.initialize()
            self.logger.info('应用程序启动')
            self.root.mainloop()
        except Exception as e:
            self.logger.critical(f'应用程序运行时发生严重错误: {str(e)}')
            raise
        finally:
            self.logger.info('应用程序关闭')

def run_application():
    """应用程序入口函数"""
    app = Application()
    app.run()

if __name__ == '__main__':
    run_application()