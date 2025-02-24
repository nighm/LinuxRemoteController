# LinuxRemoteController

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/Cursor-Team/LinuxRemoteController/releases)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

一个基于Python的Linux远程控制客户端，使用SSH协议连接并控制远程Linux服务器。

## 版本历史

### v0.1.0 (2024-01)
- 初始版本发布
- 实现基本的SSH连接和命令执行功能
- 提供图形化用户界面
- 支持密码认证方式

## 功能特点

- 图形化界面，操作简单直观
- 支持SSH密码认证
- 实时命令执行和输出显示
- 错误处理和日志记录
- 连接状态监控

## 系统要求

- Python 3.6+
- 支持Windows、Linux和macOS

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/Cursor-Team/LinuxRemoteController.git
cd LinuxRemoteController
```

2. 创建并激活虚拟环境（可选但推荐）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用说明

1. 运行程序：
```bash
python app.py
```

2. 在图形界面中输入远程服务器信息：
   - IP地址
   - 用户名
   - 密码

3. 点击"连接"按钮建立SSH连接

4. 在命令输入框中输入要执行的Linux命令

5. 点击"发送"按钮或按Enter键执行命令

6. 命令输出将显示在主窗口中

## 注意事项

- 请确保远程服务器已开启SSH服务
- 建议使用强密码保护SSH连接
- 谨慎执行高权限命令
- 定期查看日志文件了解系统运行状态

## 开发说明

### 项目结构

```
.
├── app.py          # 主程序入口
├── requirements.txt # 依赖配置
├── src/            # 源代码目录
│   ├── ssh.py      # SSH连接管理
│   └── ui.py       # 图形界面实现
└── logs/           # 日志目录
```

### 主要模块

- `app.py`: 应用程序主入口，协调SSH连接和UI交互
- `src/ssh.py`: 处理SSH连接、命令执行等核心功能
- `src/ui.py`: 实现图形用户界面

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。在提交代码前，请确保：

1. 代码符合PEP 8规范
2. 添加必要的注释和文档
3. 更新README.md（如有必要）

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 联系方式

如有任何问题或建议，请通过以下方式联系：

- Email: team@cursor.so
- GitHub Issues: https://github.com/Cursor-Team/LinuxRemoteController/issues

## 更新日志

### v1.0.0 (2024-01)

- 初始版本发布
- 基本的SSH连接和命令执行功能
- 图形化界面实现
- 支持跨平台运行（Windows/Linux/macOS）
- 完整的错误处理和日志记录功能