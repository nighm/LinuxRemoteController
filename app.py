import tkinter as tk
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from src.ui import RemoteControlUI
from src.ssh import SSHConnection

# 配置日志系统
def setup_logging():
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / 'app.log'
    handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('LinuxRemoteControl')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger

class Application:
    def __init__(self):
        self.logger = setup_logging()
        self.root = None
        self.ssh = None
        self.ui = None
    
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