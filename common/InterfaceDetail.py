from common.DataBase import DataBase


class InterfaceDetail(DataBase):
    def __init__(self):
        super().__init__()

    def getInterfaceDetail(self, url, data):
        if url == '/pro/v1/form/data/add':
            ownerId_data = self.get_random_ownerId()
            coUserId = self.get_random_coUserId(exclude_user_ids=[ownerId_data['id']])
            data.update({
                'dataList':{
                    'text_1': self.get_random_text(),
                    'ownerId': [ownerId_data],
                    'coUserId': coUserId
                },
                'ownerId': [ownerId_data],
                'coUserId': coUserId
            })
        return data





if __name__ == '__main__':
    interfaceDetail = InterfaceDetail()
    datalist = {"corpid": "ding66041eb1c6df73f535c2f4657eb6378f", "userId": "215252650523902241", "platform": "web", "appId": 0, "menuId": 0, "saasMark": 1, "formId": 8121980, "businessType": 21500, "dataId": "null", "dataList": {"text_1": "1733127766", "ownerId": [{"id": "215252650523902241", "name": "崔科达"}], "coUserId": [{"id": "136042023439277564", "name": "魏荣杰"}, {"id": "273804322726328544", "name": "林文钰"}], "date_1": 1733128036, "date_2": 1733128051, "text_4": {"text": "截止时", "value": "2", "color": "", "isVisible": 1}, "text_3": {"taskMemoText": "哈哈哈哈哈啊哈哈", "taskMemoImages": [], "taskMemoLink": [], "atUserIdList": []}, "text_5": {"text": "最高", "value": "4", "color": "#F7716C", "isVisible": 1}}, "serialNo": "", "ownerId": [{"id": "215252650523902241", "name": "崔科达"}], "coUserId": [{"id": "136042023439277564", "name": "魏荣杰"}, {"id": "273804322726328544", "name": "林文钰"}]}
    interfaceDetail.getInterfaceDetail('/pro/v1/form/data/add', datalist)