import time

from common.RandomDataBase import RandomDataBase
from common.business.TodoWork import TodoWork


class InterfaceDetail(RandomDataBase):
    def __init__(self):
        super().__init__()
        self.todowork = TodoWork()

    def pre_process_detail(self, url, data):
        if url == '/pro/v1/form/data/add':
            self.todowork.process_form_data_add(data)
        elif url == '/pro/v1/todo/list':
            self.todowork.process_todo_list(data)
        return data

    def after_process_detail(self, url, data):
        # 处理一下memberList
        if url == '/pro/v1/user/list':
            self.get_user_list(data)
        # deleteBatch接口sleep1秒
        if url == '/pro/v1/todo/deleteBatch':
            time.sleep(1)


if __name__ == '__main__':
    interfaceDetail = InterfaceDetail()
    datalist = {"corpid": "ding66041eb1c6df73f535c2f4657eb6378f", "userId": "215252650523902241", "platform": "web", "appId": 0, "menuId": 0, "saasMark": 1, "formId": 8121980, "businessType": 21500, "dataId": "null", "dataList": {"text_1": "1733127766", "ownerId": [{"id": "215252650523902241", "name": "崔科达"}], "coUserId": [{"id": "136042023439277564", "name": "魏荣杰"}, {"id": "273804322726328544", "name": "林文钰"}], "date_1": 1733128036, "date_2": 1733128051, "text_4": {"text": "截止时", "value": "2", "color": "", "isVisible": 1}, "text_3": {"taskMemoText": "哈哈哈哈哈啊哈哈", "taskMemoImages": [], "taskMemoLink": [], "atUserIdList": []}, "text_5": {"text": "最高", "value": "4", "color": "#F7716C", "isVisible": 1}}, "serialNo": "", "ownerId": [{"id": "215252650523902241", "name": "崔科达"}], "coUserId": [{"id": "136042023439277564", "name": "魏荣杰"}, {"id": "273804322726328544", "name": "林文钰"}]}
    data = interfaceDetail.pre_process_detail('/pro/v1/form/data/add', datalist)
    interfaceDetail.logger.info(data)
