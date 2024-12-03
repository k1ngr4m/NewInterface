# coding=utf-8
import datetime
import json
import pytest
import common.base as Base
from common.base import update_data_with_login_info, get_headers, find_placeholders, replace_placeholders, \
    parse_relation
from config.settings import DynamicParam
from utils.logutil import logger
from utils.readmysql import RdTestcase
from utils.requestsutil import RequestSend
from config.param import environment

case_data = RdTestcase()
case_list_negative = case_data.is_run_data('xbb', case_data.case_table_neg)
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class TestApi:
    def setup_class(self):
        logger.info(f"***** 开始执行逆向测试用例，开始时间为：{current_time} *****")

    def teardown_class(self):
        logger.info(f"***** 执行逆向测试用例完成，完成时间为：{current_time} *****")

    @pytest.mark.parametrize('case', case_list_negative)
    def test_run_negative(self, case):
        self.run(case)

    def run(self, case):
        conf_key = case_data.loadConfkey('xbb', environment)
        url = conf_key['value'] + case['url']
        headers = eval(conf_key['headers'])
        method = case['method']
        data = eval(case['request_body'])
        relation = str(case['relation'])
        case_name = case['title']

        # 更新数据中的登录信息
        key_map = {'corpid': '', 'userId': ''}
        data = update_data_with_login_info(data, key_map)

        # 处理数据和头部中的占位符
        data = replace_placeholders(data, self.get_dynamic_params())
        headers = replace_placeholders(headers, self.get_dynamic_params())

        # 添加签名到请求头
        headers = get_headers(data, headers)

        try:
            logger.info(f"正在执行 {case_name} 用例")
            res_data = RequestSend().send(url, method, data=data, headers=headers)
            logger.info(f"用例执行成功，请求的结果为\n\t{res_data}")
        except Exception as e:
            logger.error(f"用例执行失败，请查看日志。错误信息: {e}")
            assert False

        # 如果响应中有需要关联的变量，设置动态参数
        if res_data and relation != "None":
            self.set_relation(relation, res_data)

        # 断言响应结果
        self.assert_response(case, res_data)
        return res_data

    def set_relation(self, relation, res_data):
        """
        设置动态参数，用于后续用例中的占位符替换。

        :param relation: 关联字符串，格式为 "var_name=path.to.value"
        :param res_data: 响应数据
        """
        try:
            if relation:
                for rel in relation.split(","):
                    var_name, path = rel.split("=")
                    value = parse_relation(path.split("."), res_data)
                    setattr(DynamicParam, var_name, value)
                    logger.info(f"设置动态参数: {var_name}={value}")
        except Exception as e:
            logger.error(f"设置动态参数时出错: {e}")

    def get_dynamic_params(self):
        """
        获取所有动态参数，用于替换占位符。

        :return: 动态参数字典
        """
        dynamic_params = {}
        for attr in dir(DynamicParam):
            if not attr.startswith("__"):
                value = getattr(DynamicParam, attr)
                dynamic_params[attr] = value
        return dynamic_params

    def assert_response(self, case, res_data):
        """
        断言响应结果是否符合预期。

        :param case: 测试用例数据
        :param res_data: 响应数据
        """
        is_pass = False
        error_message = None  # 用于存储错误信息

        try:
            # 断言响应码不等于特定值
            actual_code = int(res_data['body']['code'])
            assert actual_code != 100001 and actual_code != 100063, f"期望状态码不等于 100001 或 100063，实际状态码 {actual_code}"
            logger.info("用例断言成功")
            is_pass = True
        except AssertionError as e:
            error_message = f"用例断言失败: {e}"
            logger.error(error_message)
        except Exception as e:
            error_message = f"用例断言时发生未知错误: {e}"
            logger.error(error_message)
        finally:
            # 使用 error_message 而不是 e
            if error_message:
                logger.error(f"最终记录: {error_message}")
            case_data.updateResults(res_data, is_pass, str(case['id']))
            assert is_pass


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_run_2neg.py'])
