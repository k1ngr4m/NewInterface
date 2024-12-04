import random

import string

from common.Base import Base
from utils.Readmysql import RdTestcase

case_data = RdTestcase()
getUser_case = case_data.load_getUser_case(case_data.case_table_pos)

class DataBase(Base):
    def __init__(self):
        super().__init__()
        self.case_data = RdTestcase()
        self.getUser_case = case_data.load_getUser_case(case_data.case_table_pos)
        # self.user_list = [{'userId': '061700090226252107', 'userName': '李智康'}, {'userId': '074102624837712380', 'userName': '闫明伟'}, {'userId': '136042023439277564', 'userName': '魏荣杰'}, {'userId': '215252650523902241', 'userName': '崔科达'}, {'userId': '273804322726328544', 'userName': '林文钰'}, {'userId': 'manager2788', 'userName': '吴琳娜'}]
        self.user_list = [] # 假设这里是一个包含所有用户的列表，每个用户是一个字典，包含 'userId' 和 'userName'
        # 定义常用汉字的列表（这里只是一个简化的例子）
        self.common_characters = "的一是了我不人在他有这们来大为国和时地之子于件发中日学男会可高自成家年以两生出能对小多然于心面进间主上社会电也使动它经现前表民得形同化方正语法所把下而工去合命力点"
        # 定义大小写字母和数字的字符集
        self.ascii_characters = string.ascii_letters + string.digits  # 包含所有大小写字母和数字

    def get_user_list(self, data):
        """
        获取该组织架构下的用户列表
        :param data: 通过接口得到的data
        :return:
        """
        result = data['body']['result']['userList']
        for item in range(len(result)):
            member = {
                'userId': result[item]['userId'],
                'userName': result[item]['name']
            }
            self.user_list.append(member)
        self.logger.info(f"获取到的用户列表为：{self.user_list}")

    def get_random_text(self, text_length=16):
        """
        生成随机文本，包含中文、英文和数字。
        :param text_length: 文本的长度
        :return: 生成的随机文本
        """
        if not isinstance(text_length, int) or text_length <= 0:
            raise ValueError("text_length must be a positive integer")
        if text_length < 3:
            raise ValueError("text_length must be at least 3 to include three Chinese characters")

        # 从常用汉字列表中随机选择前三个字符
        chinese_part = ''.join(random.choice(self.common_characters) for _ in range(3))
        # 将常用汉字和ASCII字符组合到一起
        all_characters = self.common_characters + self.ascii_characters
        # 从所有字符中随机选择剩余的字符
        remaining_length = text_length - 3
        remaining_part = ''.join(random.choice(all_characters) for _ in range(remaining_length))
        # 拼接两部分以形成最终的随机字符串
        base_text = '接口测试数据：'
        random_string = base_text + chinese_part + remaining_part

        return random_string

    def get_random_user(self):
        return random.choice(self.user_list)

    def get_random_ownerId(self):
        random_user = self.get_random_user()
        ownerId_data = {
            "id": random_user.get('userId'),
            "name": random_user.get('userName')
        }
        return ownerId_data

    def get_random_coUserId(self, count=None, exclude_user_ids=None):
        """获取指定数量的随机coUserId，确保不与exclude_user_ids中的userId相同"""
        if count is None:
            count = random.randint(1, 4)
        coUserIds_data = []
        available_users = [user for user in self.user_list if user['userId'] not in (exclude_user_ids or [])]

        if len(available_users) < count:
            count = 1
            # raise ValueError("Not enough users available to satisfy the request.")

        for _ in range(count):
            random_user = random.choice(available_users)
            coUserIds_data.append({
                "id": random_user.get('userId'),
                "name": random_user.get('userName')
            })
            # 从可用用户列表中移除已选用户，避免重复选择
            available_users.remove(random_user)

        return coUserIds_data

if __name__ == '__main__':
    db = DataBase()
    res = db.get_random_ownerId()
    print(res)