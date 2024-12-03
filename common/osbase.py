"""
文件流相关函数封装
"""
import json
import os
from utils.logutil import logger

# 没有文件则创建
def create_file(filename):
    # 获取文件的目录部分
    dir_name = os.path.dirname(filename)

    # 如果目录不存在，则创建它
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        logger.debug(f'创建目录 {dir_name}')

    # 检查文件是否存在
    if not os.path.exists(filename):
        logger.debug(f'文件不存在 {filename}')
        with open(filename, 'a', encoding='utf-8') as file:
            # 文件关闭操作实际上不需要在这里显式调用，因为with语句会自动处理
            pass
        logger.info(f"创建 {filename} 成功")
    else:
        logger.info(f"文件已存在 {filename}")



# 清空文件
def truncate_file(filename):
    try:
        with open(filename, 'r+') as file:
            file.truncate(0)
            logger.info(f"清空{filename}成功")
    except Exception as e:
        logger.error(e)


# 获取用例列表
def get_case_list(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            case_str = file.read()
            case_list = eval(case_str)
            logger.info(f"获取{filename}中的用例列表成功")
            return case_list
    except Exception as e:
        logger.error(e)


def write_file(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            result = json.dumps(data, ensure_ascii=False)
            file.write('\r')
            file.write(result)
        logger.info(f'写入{filename}成功')
    except Exception as e:
        logger.error(e)
