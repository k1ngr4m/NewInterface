import datetime
import random
import string

from common.Base import Base
from utils.Readmysql import RdTestcase

case_data = RdTestcase()
getUser_case = case_data.load_getUser_case(case_data.case_table_pos)

class RandomDataBase(Base):
    def __init__(self):
        super().__init__()
        self.case_data = RdTestcase()
        self.getUser_case = case_data.load_getUser_case(case_data.case_table_pos)
        self.user_list = [{'userId': '061700090226252107', 'userName': '李智康'}, {'userId': '074102624837712380', 'userName': '闫明伟'}, {'userId': '136042023439277564', 'userName': '魏荣杰'}, {'userId': '215252650523902241', 'userName': '崔科达'}, {'userId': '273804322726328544', 'userName': '林文钰'}, {'userId': 'manager2788', 'userName': '吴琳娜'}]
        # self.user_list = [] # 假设这里是一个包含所有用户的列表，每个用户是一个字典，包含 'userId' 和 'userName'
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

    def get_random_timestamp(self, start_timestamp=None, end_timestamp=None):
        """
        获取指定时间范围内的随机时间戳
        :param begin_time: 起始时间，默认为当前时间
        :param end_time: 结束时间，默认为当前时间
        :return: 随机时间戳
        """
        # 定义10位时间戳的起始和结束时间并转换为时间戳
        if start_timestamp is None:
            start_timestamp = int(datetime.datetime(2000, 1, 1).timestamp())  # 确保时间戳至少有10位
        if end_timestamp is None:
            end_timestamp = int(datetime.datetime(2038, 1, 19, 3, 14, 7).timestamp()) # 最大10位时间戳的时间点

        timestamp = random.randint(start_timestamp, end_timestamp)

        return timestamp

    def get_atList(self, user_list):
        """
        获取指定数量的随机atList
        :param count: 随机atList的数量，默认为None
        :return: 随机atList
        """
        # base_line = '<span class=\"at-person\">@{}&nbsp;</span>'
        base_line = ''
        for i in range(len(user_list)):
            user_name = self.get_random_user()['userName']
            base_line += f'<span class=\"at-person\">@{user_name}&nbsp;</span>'
        return base_line

    def get_random_pics(self, count=None):
        """
        获取随机图片
        :param count: 随机pics的数量，默认为None
        :return: 随机图片
        todo 图片Enum暂不处理，后续再处理
        """
        if count is None:
            count = random.randint(1, 4)
        pics = {
                "url": "https://cdn3.xbongbong.com/xbbProPrd/ding66041eb1c6df73f535c2f4657eb6378f/215252650523902241/jpg/1733362063475f0af9564bba2ce454cf189edf5f1af39.jpg",
                "uid": 1733362063472,
                "name": "整理了些暗戳戳工作号都可以用的汪汪头像_1_獭獭饲养员喵小橙_来自小红书网页版.jpg"}
        return [pics]

    def get_random_files(self, count=None):
        """
        获取随机文件
        :param count: 随机files的数量，默认为None
        :return: 随机文件
        todo 文件Enum暂不处理，后续再处理
        """
        if count is None:
            count = random.randint(1, 4)
        files = {
            "name": "整理了些暗戳戳工作号都可以用的汪汪头像_2_獭獭饲养员喵小橙_来自小红书网页版.jpg",
            "filename": "整理了些暗戳戳工作号都可以用的汪汪头像_2_獭獭饲养员喵小橙_来自小红书网页版.jpg",
            "attachIndex": "https://cdn3.xbongbong.com/xbbProPrd/ding66041eb1c6df73f535c2f4657eb6378f/215252650523902241/jpg/1733362067577107c1b958c9f6ec66af0b33b11afd670.jpg",
            "ext": "jpg",
            "size": 112447,
            "uid": 1733362067576
        }
        return [files]
if __name__ == '__main__':
    db = RandomDataBase()
    res = db.get_random_timestamp()
    res2 = db.get_random_timestamp(res)
    print(res)
    print(res2)