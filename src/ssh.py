#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SSH连接管理模块

这个模块负责处理与远程Linux服务器的SSH连接，主要功能包括：
1. 建立SSH连接
2. 执行远程命令
3. 管理连接状态
4. 处理连接错误

主要组件：
- SSHConnection类：SSH连接管理器，处理所有SSH相关操作

使用示例：
    ssh = SSHConnection()
    try:
        ssh.connect({
            'ip': '192.168.1.100',
            'username': 'root',
            'password': 'password'
        })
        output, error = ssh.execute_command('ls -l')
        print(output)
    finally:
        ssh.disconnect()

依赖：
- paramiko：SSH协议的Python实现

作者：Cursor Team
版本：0.1.0
"""

import paramiko
import logging
import socket
from typing import Dict, Tuple, Optional

class SSHConnection:
    """SSH连接管理器类
    
    处理与远程Linux服务器的SSH连接和命令执行。
    实现了连接建立、命令执行、错误处理等核心功能。
    
    属性：
        client: paramiko.SSHClient实例
        logger: 日志记录器实例
    """
    
    def __init__(self):
        """初始化SSH连接管理器
        
        创建日志记录器并初始化SSH客户端。
        初始状态下未建立连接。
        """
        self.client: Optional[paramiko.SSHClient] = None
        self.logger = logging.getLogger('LinuxRemoteControl.SSH')

    def connect(self, connection_info: Dict[str, str]) -> bool:
        """建立SSH连接

        Args:
            connection_info: 包含连接信息的字典，需要包含'ip'、'username'和'password'字段

        Returns:
            bool: 连接是否成功
        """
        try:
            self.logger.info(f'正在连接到 {connection_info["ip"]}...')
            self.logger.debug(f'连接参数: 用户名={connection_info["username"]}, IP={connection_info["ip"]}, 端口=22')
            
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.logger.debug('已创建SSH客户端实例，正在尝试建立连接...')
            
            self.client.connect(
                connection_info['ip'],
                username=connection_info['username'],
                password=connection_info['password'],
                timeout=30,  # 增加超时时间到30秒
                port=22,    # 明确指定SSH端口
                look_for_keys=False,  # 禁用密钥认证，仅使用密码认证
                banner_timeout=20  # 添加banner超时设置
            )
            self.logger.info(f'成功连接到 {connection_info["ip"]}')
            self.logger.debug('SSH会话已建立，认证成功')
            return True
        except paramiko.AuthenticationException:
            self.logger.error(f'认证失败：用户名或密码错误 (IP: {connection_info["ip"]})')
            self.client = None
            raise Exception('认证失败：用户名或密码错误')
        except socket.timeout:
            self.logger.error(f'连接超时：无法连接到服务器 (IP: {connection_info["ip"]})')
            self.client = None
            raise Exception('连接超时：请检查网络连接和服务器状态')
        except paramiko.SSHException as e:
            self.logger.error(f'SSH连接错误：{str(e)} (IP: {connection_info["ip"]})')
            self.client = None
            raise Exception(f'SSH连接错误：{str(e)}')
        except Exception as e:
            self.logger.error(f'连接失败：{str(e)} (IP: {connection_info["ip"]})')
            self.client = None
            raise Exception(f'连接失败：{str(e)}')

    def disconnect(self) -> None:
        """断开SSH连接"""
        if self.client:
            try:
                self.logger.info('正在断开SSH连接...')
                self.client.close()
                self.logger.info('SSH连接已断开')
            except Exception as e:
                self.logger.error(f'断开连接时发生错误：{str(e)}')
            finally:
                self.client = None

    def execute_command(self, command: str) -> Tuple[str, str]:
        """执行远程命令

        Args:
            command: 要执行的命令

        Returns:
            Tuple[str, str]: (标准输出, 标准错误)
        """
        if not self.is_connected:
            self.logger.error('尝试在未连接状态下执行命令')
            raise Exception('未连接到服务器')

        try:
            self.logger.debug(f'准备执行命令: {command}')
            stdin, stdout, stderr = self.client.exec_command(
                command,
                timeout=30,  # 设置命令执行超时时间
                get_pty=True  # 获取伪终端，以支持交互式命令
            )
            self.logger.debug('命令已发送，等待执行结果...')

            # 读取命令输出
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            exit_status = stdout.channel.recv_exit_status()

            self.logger.debug(f'命令执行完成，退出状态码: {exit_status}')
            if exit_status != 0:
                self.logger.warning(f'命令执行返回非零状态码: {exit_status}')
                self.logger.debug(f'错误输出: {error}')
            else:
                self.logger.debug('命令执行成功')

            return output, error

        except socket.timeout:
            self.logger.error('命令执行超时')
            raise Exception('命令执行超时，请检查命令是否正确或网络状态')
        except paramiko.SSHException as e:
            self.logger.error(f'SSH命令执行错误: {str(e)}')
            raise Exception(f'SSH命令执行错误: {str(e)}')
        except Exception as e:
            self.logger.error(f'执行命令时发生未知错误: {str(e)}')
            raise

    @property
    def is_connected(self) -> bool:
        """检查是否已连接

        Returns:
            bool: 是否已连接
        """
        return self.client is not None