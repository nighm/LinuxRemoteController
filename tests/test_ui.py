#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户界面模块单元测试

测试图形界面的核心功能，包括：
1. 界面初始化
2. 事件处理
3. 输出显示
4. 错误提示

作者：Cursor Team
版本：0.1.0
"""

import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from src.ui import RemoteControlUI

class TestRemoteControlUI(unittest.TestCase):
    """用户界面测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.root = tk.Tk()
        self.mock_on_connect = Mock()
        self.mock_on_disconnect = Mock()
        self.mock_on_send_command = Mock()
        
        self.ui = RemoteControlUI(
            self.root,
            on_connect=self.mock_on_connect,
            on_disconnect=self.mock_on_disconnect,
            on_send_command=self.mock_on_send_command
        )
    
    def tearDown(self):
        """测试后清理"""
        self.root.destroy()
    
    def test_init(self):
        """测试界面初始化"""
        # 验证基本组件是否存在
        self.assertIsNotNone(self.ui.connection_frame)
        self.assertIsNotNone(self.ui.command_frame)
        self.assertIsNotNone(self.ui.terminal_frame)
        
        # 验证输入字段
        self.assertIsNotNone(self.ui.ip_entry)
        self.assertIsNotNone(self.ui.username_entry)
        self.assertIsNotNone(self.ui.password_entry)
        self.assertIsNotNone(self.ui.command_entry)
    
    def test_connect_button_click(self):
        """测试连接按钮点击事件"""
        # 设置测试数据
        self.ui.ip_entry.insert(0, '192.168.1.100')
        self.ui.username_entry.insert(0, 'test_user')
        self.ui.password_entry.insert(0, 'test_password')
        
        # 模拟点击连接按钮
        self.ui.connect_btn.invoke()
        
        # 验证回调函数调用
        self.mock_on_connect.assert_called_once_with({
            'ip': '192.168.1.100',
            'username': 'test_user',
            'password': 'test_password'
        })
    
    def test_disconnect_button_click(self):
        """测试断开连接按钮点击事件"""
        # 先设置按钮为已连接状态
        self.ui.connect_btn.config(text='断开')
        
        # 模拟点击断开连接按钮
        self.ui.connect_btn.invoke()
        
        # 验证回调函数调用
        self.mock_on_disconnect.assert_called_once()
        
        # 验证按钮文本是否恢复为连接
        self.assertEqual(self.ui.connect_btn['text'], '连接')
    
    def test_send_command_button_click(self):
        """测试发送命令按钮点击事件"""
        # 设置测试命令
        test_command = 'ls -l'
        self.ui.command_entry.insert(0, test_command)
        
        # 模拟点击发送命令按钮
        self.ui.send_btn.invoke()
        
        # 验证回调函数调用
        self.mock_on_send_command.assert_called_once_with(test_command)
        
        # 验证命令输入框是否被清空
        self.assertEqual(self.ui.command_entry.get(), '')
    
    def test_append_output(self):
        """测试输出显示功能"""
        test_output = 'Test output message'
        self.ui.append_output(test_output)
        
        # 验证输出是否正确显示
        output_text = self.ui.output_text.get('1.0', tk.END).strip()
        self.assertEqual(output_text, test_output)
    
    @patch('tkinter.messagebox.showerror')
    def test_show_error(self, mock_showerror):
        """测试错误提示功能"""
        title = 'Error'
        message = 'Test error message'
        self.ui.show_error(title, message)
        
        # 验证错误提示框是否正确显示
        mock_showerror.assert_called_once_with(title, message)
    
if __name__ == '__main__':
    unittest.main()