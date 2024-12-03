# coding=utf-8
import datetime
import json
from utils.mysqlutil import MysqlUtil
from utils.logutil import logger

mysql = MysqlUtil()


class RdTestcase:
    def __init__(self):
        self.case_table_pos = 'test_case_list_pos'
        self.case_table_neg = 'test_case_list_neg'

    # 加载正向测试用例
    def load_test_case(self, web, table_name):
        sql = f"select * from {table_name} where web = '{web}'"
        results = mysql.get_fetchall(sql)
        return results

    # 筛选可执行的用例
    def is_run_data(self, web, table_name):
        run_list = [case for case in self.load_test_case(web, table_name) if case['isdel'] == 1]
        return run_list

    # 获取配置信息
    def loadConfkey(self, web, environment):
        sql = f"select * from test_config where web='{web}' and environment='{environment}'"
        results = mysql.get_fetchone(sql)
        return results

    # 更新测试结果
    def updateResults(self, response, is_pass, case_id):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = f"insert into test_result_record (case_id,times,response,result) values ('{case_id}','{current_time}','{json.dumps(response, ensure_ascii=False)}','{is_pass}')"
        rows = mysql.sql_execute(sql)
        # logger.debug(sql)
        return rows

    def truncateTable(self, table):
        sql = f"truncate table {table}"
        rows = mysql.sql_execute(sql)
        # logger.debug(sql)
        return rows

    def update_case_from_yapi(self, case_table_name, id, title, url, method, request_body, relation, expected_code, isdel):
        sql = f"insert into {case_table_name} (id,web,title,url,method,request_body,request_type,relation,expected_code,isdel) value ('{id}','xbb','{title}','{url}','{method}','{request_body}','json','{relation}',{expected_code},{isdel})"
        rows = mysql.sql_execute(sql)
        # logger.debug(sql)
        return rows


if __name__ == '__main__':
    test = RdTestcase()
    url = test.loadConfkey('xbb', 'url_api')['value']
    print(url)
