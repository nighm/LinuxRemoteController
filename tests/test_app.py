#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
应用程序主模块集成测试

测试应用程序的核心功能和组件交互，包括：
1. 应用程序初始化
2. 日志系统配置
3. UI和SSH连接的集成
4. 错误处理和异常恢复

作者：Cursor Team
版本：0.1.0
"""

import unittest
from unittest.mock import Mock, patch
import tkinter as tk
import logging
from pathlib import Path
from app import Application, setup_logging

class TestApplication(unittest.TestCase):
    """应用程序集成测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.app = Application()
    
    def tearDown(self):
        """测试后清理"""
        if self.app.root:
            self.app.root.destroy()
    
    def test_setup_logging(self):
        """测试日志系统配置"""
        logger = setup_logging()
        
        # 验证日志配置
        self.assertEqual(logger.name, 'LinuxRemoteControl')
        self.assertEqual(logger.level, logging.INFO)
        
        # 验证日志文件创建
        log_file = Path('logs/app.log')
        self.assertTrue(log_file.exists())
    
    def test_application_init(self):
        """测试应用程序初始化"""
        self.app.initialize()
        
        # 验证组件初始化
        self.assertIsNotNone(self.app.root)
        self.assertIsNotNone(self.app.ssh)
        self.assertIsNotNone(self.app.ui)
        
        # 验证窗口标题
        self.assertEqual(self.app.root.title(), 'Linux远程控制客户端')
    
    @patch('src.ssh.SSHConnection')
    def test_handle_connect(self, mock_ssh_connection):
        """测试连接处理"""
        self.app.initialize()
        
        # 配置Mock
        mock_ssh = Mock()
        mock_ssh_connection.return_value = mock_ssh
        self.app.ssh = mock_ssh
        
        # 测试成功连接
        connection_info = {
            'ip': '192.168.1.100',
            'username': 'test_user',
            'password': 'test_password'
        }
        result = self.app._handle_connect(connection_info)
        
        # 验证结果
        self.assertTrue(result)
        mock_ssh.connect.assert_called_once_with(connection_info)
    
    @patch('src.ssh.SSHConnection')
    def test_handle_disconnect(self, mock_ssh_connection):
        """测试断开连接处理"""
        self.app.initialize()
        
        # 配置Mock
        mock_ssh = Mock()
        mock_ssh_connection.return_value = mock_ssh
        self.app.ssh = mock_ssh
        
        # 测试断开连接
        self.app._handle_disconnect()
        
        # 验证结果
        mock_ssh.disconnect.assert_called_once()
    
    @patch('src.ssh.SSHConnection')
    def test_handle_send_command(self, mock_ssh_connection):
        """测试命令发送处理"""
        self.app.initialize()
        
        # 配置Mock
        mock_ssh = Mock()
        mock_ssh.is_connected = True
        mock_ssh.execute_command.return_value = ('command output', '')
        mock_ssh_connection.return_value = mock_ssh
        self.app.ssh = mock_ssh
        
        # 测试发送命令
        test_command = 'ls -l'
        self.app._handle_send_command(test_command)
        
        # 验证结果
        mock_ssh.execute_command.assert_called_once_with(test_command)
    
    @patch('src.ssh.SSHConnection')
    def test_error_handling(self, mock_ssh_connection):
        """测试错误处理"""
        self.app.initialize()
        
        # 配置Mock抛出异常
        mock_ssh = Mock()
        mock_ssh.connect.side_effect = Exception('Connection failed')
        mock_ssh_connection.return_value = mock_ssh
        self.app.ssh = mock_ssh
        
        # 测试连接错误处理
        connection_info = {
            'ip': '192.168.1.100',
            'username': 'test_user',
            'password': 'test_password'
        }
        result = self.app._handle_connect(connection_info)
        
        # 验证结果
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()