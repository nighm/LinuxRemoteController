import paramiko
from typing import Dict, Tuple, Optional

class SSHConnection:
    def __init__(self):
        self.client: Optional[paramiko.SSHClient] = None

    def connect(self, connection_info: Dict[str, str]) -> bool:
        """建立SSH连接

        Args:
            connection_info: 包含连接信息的字典，需要包含'ip'、'username'和'password'字段

        Returns:
            bool: 连接是否成功
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                connection_info['ip'],
                username=connection_info['username'],
                password=connection_info['password'],
                timeout=10,  # 添加超时设置
                port=22,    # 明确指定SSH端口
                look_for_keys=False  # 禁用密钥认证，仅使用密码认证
            )
            return True
        except Exception as e:
            self.client = None
            raise e

    def disconnect(self) -> None:
        """断开SSH连接"""
        if self.client:
            self.client.close()
            self.client = None

    def execute_command(self, command: str) -> Tuple[str, str]:
        """执行SSH命令

        Args:
            command: 要执行的命令

        Returns:
            Tuple[str, str]: 命令的输出和错误信息

        Raises:
            Exception: 如果命令执行失败
        """
        if not self.client:
            raise Exception('未建立连接')

        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    @property
    def is_connected(self) -> bool:
        """检查是否已连接

        Returns:
            bool: 是否已连接
        """
        return self.client is not None