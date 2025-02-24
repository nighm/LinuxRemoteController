# 贡献指南

感谢您对LinuxRemoteController项目的关注！我们欢迎任何形式的贡献，包括但不限于：

- 报告问题（Issues）
- 提交改进建议
- 提交代码（Pull Requests）
- 完善文档

## 提交Issue

1. 在提交Issue前，请先搜索是否已存在相似的Issue
2. 使用清晰的标题描述问题
3. 提供以下信息：
   - 问题描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 运行环境（操作系统、Python版本等）
   - 错误日志（如有）

## 提交Pull Request

1. Fork本仓库
2. 创建新的分支：`git checkout -b feature/your-feature-name`
3. 提交您的改动：`git commit -m 'Add some feature'`
4. 推送到您的Fork仓库：`git push origin feature/your-feature-name`
5. 提交Pull Request

### 代码规范

- 遵循PEP 8 Python代码风格指南
- 添加必要的注释和文档字符串
- 确保代码通过所有测试
- 新功能需要添加相应的测试用例

### 提交信息规范

提交信息格式：
```
<类型>: <描述>

[可选的详细描述]

[可选的关闭Issue引用]
```

类型包括：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

示例：
```
feat: 添加SSH密钥认证支持

- 实现RSA密钥对认证
- 添加密钥管理界面

Closes #123
```

## 开发流程

1. 创建并激活虚拟环境
2. 安装开发依赖：`pip install -r requirements-dev.txt`
3. 进行代码修改
4. 运行测试：`python -m pytest`
5. 提交代码前进行代码格式检查：`flake8`

## 发布流程

1. 更新版本号（遵循语义化版本规范）
2. 更新CHANGELOG.md
3. 创建新的Release标签

## 许可证

通过提交代码，您同意将代码以MIT许可证的方式贡献给项目。

## 联系方式

如有任何问题，请通过以下方式联系我们：

- 提交Issue
- 发送邮件至：team@cursor.so

再次感谢您的贡献！