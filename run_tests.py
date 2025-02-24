#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试运行脚本

这个脚本用于执行所有单元测试和集成测试，并生成测试覆盖率报告。
使用方法：
    python run_tests.py

作者：Cursor Team
版本：0.1.0
"""

import unittest
import coverage
import sys
from pathlib import Path

def run_tests_with_coverage():
    """运行测试并生成覆盖率报告"""
    # 初始化覆盖率收集器
    cov = coverage.Coverage(
        branch=True,
        source=['src', 'app.py'],
        omit=['*/__init__.py', 'tests/*']
    )
    
    # 开始收集覆盖率数据
    cov.start()
    
    # 发现并运行所有测试
    test_loader = unittest.TestLoader()
    test_dir = Path(__file__).parent / 'tests'
    suite = test_loader.discover(str(test_dir))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 停止覆盖率收集
    cov.stop()
    cov.save()
    
    # 生成报告
    print('\n生成测试覆盖率报告...')
    cov.report()
    
    # 生成HTML报告
    report_dir = Path('coverage_report')
    report_dir.mkdir(exist_ok=True)
    cov.html_report(directory=str(report_dir))
    
    print(f'\nHTML格式的详细报告已生成到: {report_dir}')
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests_with_coverage()
    sys.exit(0 if success else 1)