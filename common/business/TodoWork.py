import random

from common.RandomDataBase import RandomDataBase


class TodoWork(RandomDataBase):
    def __init__(self):
        super().__init__()

    def process_form_data_add(self, form_data):
        """
        处理表单数据
        :param form_data: 表单数据
        :return: 处理后的表单数据
        """
        ownerId_data = self.get_random_ownerId()
        coUserId = self.get_random_coUserId(exclude_user_ids=[ownerId_data['id']])
        start_timestamp = self.get_random_timestamp()
        end_timestamp = self.get_random_timestamp(start_timestamp=start_timestamp)
        form_data['dataList'].update({
            'text_1': self.get_random_text(),
            'ownerId': [ownerId_data],
            'coUserId': coUserId,
            'date_1': start_timestamp,
            'date_2': end_timestamp,
            'text_3': self.get_random_text3(coUserId),
            'text_4': self.get_random_text4(),
            'text_5': self.get_random_text5(),
        })
        form_data.update({
            'ownerId': [ownerId_data],
            'coUserId': coUserId
        })
        return form_data

    def get_random_text3(self, atUser_list=None):
        """
        随机生成任务描述字段
        :return: 任务描述字段的值(text3)
        """
        if atUser_list is None:
            atUser_list = self.get_random_coUserId()
        text3 = {
            'taskMemoText': self.get_atList(atUser_list) + self.get_random_text(1500),
            'taskMemoImages': self.get_random_pics(),
            'taskMemoLink': self.get_random_files(),
            'atUserIdList': atUser_list
        }
        return text3

    def get_random_text4(self):
        """
        随机生成任务截止提醒字段
        :return:任务截止提醒字段的值(text4)
        """
        items = [
            {"text": "无提醒", "value": "1", "color": "#646566"},
            {"text": "截止时", "value": "2", "color": "#646566"},
            {"text": "截止前15分钟", "value": "3", "color": "#646566"},
            {"text": "截止前30分钟", "value": "4", "color": "#646566"},
            {"text": "截止前1小时", "value": "5", "color": "#646566"},
            {"text": "截止前1天", "value": "6", "color": "#646566"}
        ]
        return random.choice(items)

    def get_random_text5(self):
        """
        随机生成任务优先级
        :return:任务优先级字段的值(text5)
        """
        items = [
            {"color": "#646566", "isVisible": 1, "text": "低", "value": "1"},
            {"color": "#4DACFF", "isVisible": 1, "text": "中", "value": "2"},
            {"color": "#FFB521", "isVisible": 1, "text": "高", "value": "3"},
            {"color": "#F7716C", "isVisible": 1, "text": "最高", "value": "4" }
        ]
        return random.choice(items)
