import requests as requests
from utils.readmysql import RdTestcase
from utils.logutil import logger
import commom.osbase as osbase
from utils.createcaseutil import CreateCase


positive_case_file = r'utils/data/positive_case.json'
negative_case_file = r"utils/data/negative_case.json"

cr = CreateCase()
sql = RdTestcase()
url = 'http://1.15.174.185:3001'
# token = '962fd4813aa01538ad26ef57555738e4e7c485d5ca656e70be723bb5a35afa4f'
token = 'b1f452f0548fc22e45dae451559318279168d085ab2f63b59a82bc5251ef71e9'

class Yapi:
    def __init__(self):
        self.id = 0

    # 获取菜单列表
    def get_cat_menu(self):
        urls = url + '/api/interface/getCatMenu'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'project_id': 11,  # 项目id
            'token': token
        }
        cat_id_list = []
        try:
            response = requests.get(url=urls, params=body, headers=headers).json()
            errcode = response['errcode']
            # 成功获取data
            if errcode == 0:
                data = response['data']
                for i in range(len(data)):
                    cat_id = data[i]['_id']
                    name = data[i]['name']
                    # print(data[i])
                    # 打印项目信息
                    logger.debug(f'cat_id:{cat_id}\t\tname:{name}')
                    cat_id_list.append(cat_id)
            # 返回数据错误
            else:
                print(errcode)
        except Exception as e:
            print(e)
        return cat_id_list

    def get_interface_list_cat(self, cat_id_list):
        urls = url + '/api/interface/list_cat'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        interface_data_list = []
        for i in range(len(cat_id_list)):
            body = {
                'catid': cat_id_list[i],  # 分组id
                'token': token,
                'page': 1,
                'limit': 50
            }
            try:
                response = requests.get(url=urls, params=body, headers=headers).json()
                if response['errcode'] == 0:
                    data = response['data']
                    data_list = data['list']
                    for j in range(len(data_list)):
                        interface_id = data_list[j]['_id']
                        data_dict = self.get_interface_detail(interface_id)
                        self.id = self.id + 1
                        data_dict['id'] = self.id
                        interface_data_list.append(data_dict)
                else:
                    logger.error(response['errcode'])
            except Exception as e:
                logger.error(e)
        logger.debug(f'获取{len(interface_data_list)}条接口数据')
        return interface_data_list

    def get_interface_detail(self, interface_id):
        urls = url + '/api/interface/get'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'id': interface_id,  # 接口id
            'token': token
        }
        try:
            response = requests.get(url=urls, params=body, headers=headers).json()
            if response['errcode'] == 0:
                data = response['data']
                method = str(data['method']).lower()
                title = data['title']
                path = data['path']
                req_body_other = eval(data['req_body_other'])
                relation = data['markdown']
                status = data['status']

                if status == 'done':
                    status = int(1)
                else:
                    status = int(0)

                interface_data_dict = {
                    'id': 0,
                    'title': title,
                    'method': method,
                    'path': path,
                    'req_body': req_body_other,
                    'relation': relation,
                    'expected_code': 1,
                    'isdel': status
                }
                return interface_data_dict
            else:
                print(response['errcode'])
        except Exception as e:
            print(e)

    def save_positive_data_list(self):
        cat_id_list = self.get_cat_menu()
        interface_data_list = self.get_interface_list_cat(cat_id_list)
        osbase.create_file(positive_case_file)
        osbase.write_file(positive_case_file, interface_data_list)

    def update_database(self, table_name, file_name):
        sql.truncateTable(table_name)
        case_list = osbase.get_case_list(file_name)
        for i in range(len(case_list)):
            case_dict = case_list[i]
            id = case_dict['id']
            title = case_dict['title']
            method = case_dict['method']
            url = case_dict['path']
            request_body = str(case_dict['req_body']).replace("'", '"').replace('"None"', 'None').replace('"False"',
                                                                                                          'False').replace(
                '"True"', 'True')
            relation = case_dict['relation']
            expected_code = case_dict['expected_code']
            isdel = case_dict['isdel']
            sql.update_case_from_yapi(table_name, id, title, url, method, request_body, relation, expected_code,
                                      isdel)
        logger.info(f'写入数据库{table_name}成功')

    def update_positive_database(self):
        self.save_positive_data_list()
        self.update_database(sql.case_table_pos, positive_case_file)

    def update_negative_database(self):
        cr.create_negative_case()
        self.update_database(sql.case_table_neg, negative_case_file)


if __name__ == '__main__':
    yapi = Yapi()
    # yapi.get_cat_menu()
    yapi.update_positive_database()
    # yapi.save_positive_data_list()