#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SSH连接模块单元测试

测试SSH连接管理器的核心功能，包括：
1. 连接建立和断开
2. 命令执行
3. 错误处理
4. 连接状态管理

作者：Cursor Team
版本：0.1.0
"""

import unittest
from unittest.mock import Mock, patch
from src.ssh import SSHConnection
import paramiko

class TestSSHConnection(unittest.TestCase):
    """SSH连接管理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.ssh = SSHConnection()
        self.test_connection_info = {
            'ip': '192.168.1.100',
            'username': 'test_user',
            'password': 'test_password'
        }
    
    def tearDown(self):
        """测试后清理"""
        if self.ssh.client:
            self.ssh.disconnect()
    
    @patch('paramiko.SSHClient')
    def test_connect_success(self, mock_ssh_client):
        """测试SSH连接成功场景"""
        # 配置Mock
        mock_client = Mock()
        mock_ssh_client.return_value = mock_client
        
        # 执行测试
        result = self.ssh.connect(self.test_connection_info)
        
        # 验证结果
        self.assertTrue(result)
        mock_client.connect.assert_called_once_with(
            self.test_connection_info['ip'],
            username=self.test_connection_info['username'],
            password=self.test_connection_info['password'],
            timeout=10,
            port=22,
            look_for_keys=False
        )
    
    @patch('paramiko.SSHClient')
    def test_connect_auth_failure(self, mock_ssh_client):
        """测试SSH认证失败场景"""
        # 配置Mock抛出认证异常
        mock_client = Mock()
        mock_client.connect.side_effect = paramiko.AuthenticationException()
        mock_ssh_client.return_value = mock_client
        
        # 执行测试并验证异常
        with self.assertRaises(Exception) as context:
            self.ssh.connect(self.test_connection_info)
        
        self.assertEqual(str(context.exception), '认证失败：用户名或密码错误')
    
    @patch('paramiko.SSHClient')
    def test_execute_command_success(self, mock_ssh_client):
        """测试命令执行成功场景"""
        # 配置Mock
        mock_client = Mock()
        mock_stdout = Mock()
        mock_stderr = Mock()
        mock_stdout.read.return_value = b'command output'
        mock_stderr.read.return_value = b''
        mock_client.exec_command.return_value = (None, mock_stdout, mock_stderr)
        mock_ssh_client.return_value = mock_client
        
        # 连接并执行命令
        self.ssh.connect(self.test_connection_info)
        output, error = self.ssh.execute_command('test command')
        
        # 验证结果
        self.assertEqual(output, 'command output')
        self.assertEqual(error, '')
        mock_client.exec_command.assert_called_once_with('test command')
    
    def test_execute_command_not_connected(self):
        """测试未连接时执行命令场景"""
        with self.assertRaises(Exception) as context:
            self.ssh.execute_command('test command')
        
        self.assertEqual(str(context.exception), '未建立连接')
    
    @patch('paramiko.SSHClient')
    def test_disconnect(self, mock_ssh_client):
        """测试断开连接"""
        # 配置Mock
        mock_client = Mock()
        mock_ssh_client.return_value = mock_client
        
        # 建立连接后断开
        self.ssh.connect(self.test_connection_info)
        self.ssh.disconnect()
        
        # 验证结果
        mock_client.close.assert_called_once()
        self.assertIsNone(self.ssh.client)
    
    @patch('paramiko.SSHClient')
    def test_is_connected(self, mock_ssh_client):
        """测试连接状态检查"""
        # 初始状态应为未连接
        self.assertFalse(self.ssh.is_connected)
        
        # 建立连接后应为已连接
        mock_client = Mock()
        mock_ssh_client.return_value = mock_client
        self.ssh.connect(self.test_connection_info)
        self.assertTrue(self.ssh.is_connected)
        
        # 断开连接后应为未连接
        self.ssh.disconnect()
        self.assertFalse(self.ssh.is_connected)

if __name__ == '__main__':
    unittest.main()