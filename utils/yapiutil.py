import json
import requests
from utils.readmysql import RdTestcase
from utils.logutil import logger
from common.osbase import create_file, write_file, get_case_list  # 假设这些方法存在于commom.osbase模块中
from utils.createcaseutil import CreateCase

# 接口文件路径
POSITIVE_CASE_FILE = 'utils/data/positive_case.json'
NEGATIVE_CASE_FILE = "utils/data/negative_case.json"

# YAPI服务地址和认证token
YAPI_URL = 'http://1.15.174.185:3001'
YAPI_TOKEN = 'b1f452f0548fc22e45dae451559318279168d085ab2f63b59a82bc5251ef71e9'


class Yapi:
    def __init__(self):
        self.create_case = CreateCase()
        self.sql = RdTestcase()
        self.id_counter = 0  # 用于生成唯一ID

    # 发送GET请求到YAPI
    def _get_yapi(self, endpoint, params):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.get(YAPI_URL + endpoint, params=params, headers=headers).json()
        if response['errcode'] != 0:
            logger.error(f"Error from YAPI: {response['errmsg']}")
            return None
        return response['data']

    # 获取菜单列表
    def get_cat_menu(self):
        cat_id_list = []
        data = self._get_yapi('/api/interface/getCatMenu', {'project_id': 11, 'token': YAPI_TOKEN})
        if data:
            for item in data:
                cat_id = item['_id']
                name = item['name']
                logger.debug(f'cat_id:{cat_id}\t\tname:{name}')
                cat_id_list.append(cat_id)
        return cat_id_list

    # 获取接口详情
    def get_interface_detail(self, interface_id):
        data = self._get_yapi('/api/interface/get', {'id': interface_id, 'token': YAPI_TOKEN})
        if not data:
            logger.error(f"Failed to fetch interface detail for id: {interface_id}")
            return None

        try:
            method = data['method'].lower()
            title = data['title']
            path = data['path']
            req_body_other_raw = data.get('req_body_other', '{}')  # 使用get方法并提供默认值以防键不存在
            relation = data.get('markdown', '')  # 同样地，防止键不存在
            status = int(1) if data.get('status') == 'done' else int(0)

            # 尝试解析req_body_other，若失败则记录错误信息并设置为空字典
            try:
                req_body_other = json.loads(req_body_other_raw.replace("null", '"null"').replace('true', '"true"').replace('false','"false"'))
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse req_body_other for interface {interface_id}: {e}")
                req_body_other = {}

            # 更新ID计数器，并将其作为新接口数据的一部分
            self.id_counter += 1
            interface_data_dict = {
                'id': self.id_counter,
                'title': title,
                'method': method,
                'path': path,
                'req_body': req_body_other,
                'relation': relation,
                'expected_code': 1,
                'isdel': status
            }
            return interface_data_dict

        except KeyError as e:
            logger.error(f"Missing key in interface detail for id {interface_id}: {e}")
            return None

    # 获取分类下的所有接口列表
    def get_interface_list_cat(self, cat_id_list):
        interfaces = []
        for cat_id in cat_id_list:
            data = self._get_yapi('/api/interface/list_cat',
                                  {'catid': cat_id, 'token': YAPI_TOKEN, 'page': 1, 'limit': 50})
            if data and 'list' in data:
                for item in data['list']:
                    detail = self.get_interface_detail(item['_id'])
                    if detail:
                        interfaces.append(detail)
        logger.debug(f'获取{len(interfaces)}条接口数据')
        return interfaces

    # 保存正面用例到文件
    def save_positive_data_list(self):
        create_file(POSITIVE_CASE_FILE)
        write_file(POSITIVE_CASE_FILE, self.get_interface_list_cat(self.get_cat_menu()))

    # 更新数据库表
    def update_database(self, table_name, file_name):
        self.sql.truncateTable(table_name)
        case_list = get_case_list(file_name)
        for case in case_list:
            request_body = str(case['req_body']).replace("'", '"').replace('"None"', 'None').replace('"False',
                                                                                                     'False').replace(
                '"True"', 'True')
            self.sql.update_case_from_yapi(
                table_name,
                case['id'],
                case['title'],
                case['path'],
                case['method'],
                request_body,
                case['relation'],
                case['expected_code'],
                case['isdel']
            )
        logger.info(f'写入数据库{table_name}成功')

    # 更新正面用例数据库
    def update_positive_database(self):
        self.save_positive_data_list()
        self.update_database(self.sql.case_table_pos, POSITIVE_CASE_FILE)

    # 更新负面用例数据库
    def update_negative_database(self):
        self.create_case.create_negative_case()
        self.update_database(self.sql.case_table_neg, NEGATIVE_CASE_FILE)

if __name__ == '__main__':
    yapi = Yapi()
    yapi.update_positive_database()