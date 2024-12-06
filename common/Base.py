# coding=utf-8
import random

import string

import hashlib
import json
from string import Template
import re
from config.param import login_para
from utils.Logutil import logger

class Base(object):
    def __init__(self):
        self.logger = logger

    def create_sign_code(self, params, token):
        """
        根据请求参数和生产令牌生成签名值。

        :param params: 请求参数字典
        :param token: 生产环境访问令牌
        :return: 签名字符串
        """
        sign_str = json.dumps(params) + str(token)
        return hashlib.sha256(sign_str.encode('utf-8')).hexdigest()

    def get_login_info(self):
        """
        从配置中获取登录信息。

        :return: 登录信息字典，如果解析失败则返回空字典
        """
        try:
            return json.loads(login_para) if login_para else {}
        except Exception as e:
            print(f"解析登录参数时出错: {e}")
            return {}

    def update_data_with_login_info(self, data, key_map):
        """
        使用登录信息更新数据字典中的特定键。

        :param data: 要更新的数据字典
        :param key_map: 包含需要替换的键和默认值的映射
        :return: 更新后的数据字典
        """
        login_info = self.get_login_info()
        for key, default in key_map.items():
            data[key] = login_info.get(key, default)
        return data

    def get_headers(self, data, headers):
        """
        为请求头添加签名。

        :param data: 请求体数据
        :param headers: 请求头字典
        :return: 包含签名的请求头字典
        """
        login_info = self.get_login_info()
        login_token = login_info.get('xbbAccessToken', '')
        headers['sign'] = self.create_sign_code(data, login_token)
        return headers

    def find_placeholders(self, data):
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

    def replace_placeholders(self, ori_data, replace_dict):
        """
        替换数据中的占位符为实际值。

        :param ori_data: 原始数据，可以是包含占位符的字典或字符串
        :param replace_dict: 占位符到实际值的映射字典
        :return: 替换后的数据
        """
        data_str = json.dumps(ori_data)
        template = Template(data_str)
        return json.loads(template.safe_substitute(replace_dict))

    def parse_relation(self, var_list, resdata):
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
                    return self.parse_relation(var_list, result)
        elif isinstance(resdata, dict):
            return self.parse_relation(var_list, resdata.get(current_key))

        return None

    def trans_str_bool(self, string):
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

    def trans_str_str(self, string):
        return (str(string)
                .replace("'", '"')
                .replace('"None"', 'None')
                .replace('"False','False')
                .replace('"True"', 'True'))

    def trans_bool_str(self, string):
        """
        将Python布尔值和None转换为JSON兼容的字符串表示。

        :param string: 需要转换的字符串
        :return: 转换后的字符串
        """
        return (str(string)
                .replace("null", '"null"')
                .replace('true', '"true"')
                .replace('false','"false"'))

if __name__ == '__main__':
    # 示例：使用replace_placeholders函数替换占位符
    bs = Base()
    # original_data = {"admin-token": "${token}"}
    # replacement_data = {'token': 'k1ngr4m'}
    # print(bs.replace_placeholders(original_data, replacement_data))
    para = {"corpid":"ding66041eb1c6df73f535c2f4657eb6378f","userId":"215252650523902241","platform":"web","businessType":21500}
    token = "29914dde2c97c0a0c9f9936beb161445b00bd1e3651b01f82413d70036d2c368"
    sign = bs.create_sign_code(para,token)
    print(sign)
