# conftest.py
import pytest
from datetime import datetime
import os


def pytest_configure(config):
    # 获取当前日期和时间并构造报告文件名
    now = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    report_filename = f'testcase/reports/{now}.report.html'

    # 动态添加 --html 参数
    config.option.htmlpath = report_filename

    # 确保 reports 目录存在
    os.makedirs(os.path.dirname(report_filename), exist_ok=True)

    # 设置其他选项，如标题
    config.option.title = 'xbb接口自动化测试报告'

    # 如果你想确保报告是自包含的（所有资源嵌入到HTML文件中），可以设置 --self-contained-html
    config.option.self_contained_html = True


# 使用 pytest_html.environment 来添加元数据
def pytest_html_report_title(report):
    report.title = "xbb接口自动化测试报告"
