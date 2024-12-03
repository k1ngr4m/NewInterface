# coding=utf-8
import hashlib
import json
from string import Template
import re
from config.param import login_para

def create_sign_code(params, token):
    """
    根据请求参数和生产令牌生成签名值。

    :param params: 请求参数字典
    :param token: 生产环境访问令牌
    :return: 签名字符串
    """
    sign_str = json.dumps(params) + str(token)
    return hashlib.sha256(sign_str.encode('utf-8')).hexdigest()

def get_login_info():
    """
    从配置中获取登录信息。

    :return: 登录信息字典，如果解析失败则返回空字典
    """
    try:
        return json.loads(login_para) if login_para else {}
    except Exception as e:
        print(f"解析登录参数时出错: {e}")
        return {}

def update_data_with_login_info(data, key_map):
    """
    使用登录信息更新数据字典中的特定键。

    :param data: 要更新的数据字典
    :param key_map: 包含需要替换的键和默认值的映射
    :return: 更新后的数据字典
    """
    login_info = get_login_info()
    for key, default in key_map.items():
        data[key] = login_info.get(key, default)
    return data

def get_headers(data, headers):
    """
    为请求头添加签名。

    :param data: 请求体数据
    :param headers: 请求头字典
    :return: 包含签名的请求头字典
    """
    login_info = get_login_info()
    login_token = login_info.get('xbbAccessToken', '')
    headers['sign'] = create_sign_code(data, login_token)
    return headers

def find_placeholders(data):
    """
    查找数据中的占位符。

    :param data: 字典或字符串形式的数据
    :return: 占位符列表
    """
    if isinstance(data, dict):
        data_str = json.dumps(data)
        pattern = r"\${(.*?)}"
        return re.findall(pattern, data_str)
    return []

def replace_placeholders(ori_data, replace_dict):
    """
    替换数据中的占位符为实际值。

    :param ori_data: 原始数据，可以是包含占位符的字典或字符串
    :param replace_dict: 占位符到实际值的映射字典
    :return: 替换后的数据
    """
    data_str = json.dumps(ori_data)
    template = Template(data_str)
    return json.loads(template.safe_substitute(replace_dict))

def parse_relation(var_list, resdata):
    """
    根据提供的路径列表解析JSON数据。

    :param var_list: JSON路径列表
    :param resdata: JSON格式的数据
    :return: 解析后的值
    """
    if not var_list or not isinstance(resdata, (dict, list)):
        return resdata

    current_key = var_list.pop(0)
    if isinstance(resdata, list):
        for item in resdata:
            result = item.get(current_key)
            if result is not None:
                return parse_relation(var_list, result)
    elif isinstance(resdata, dict):
        return parse_relation(var_list, resdata.get(current_key))

    return None

def trans_str_bool(string):
    """
    将Python布尔值和None转换为JSON兼容的字符串表示。

    :param string: 需要转换的字符串
    :return: 转换后的字符串
    """
    return (str(string)
            .replace("'", '"')
            .replace('None', 'null')
            .replace('False', 'false')
            .replace('True', 'true'))

if __name__ == '__main__':
    # 示例：使用replace_placeholders函数替换占位符
    original_data = {"admin-token": "${token}"}
    replacement_data = {'token': 'k1ngr4m'}
    print(replace_placeholders(original_data, replacement_data))