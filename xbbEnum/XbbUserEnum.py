import random

from enum import Enum

# 使用Enum存人员数据用于生成接口中的成员数据，但是不够灵活
class XbbUserEnum(Enum):
    WEI_RONGJIE = ("136042023439277564", "魏荣杰")
    LIN_WENYU = ("273804322726328544", "林文钰")
    CUI_KEDA = ("215252650523902241", "崔科达")

    @classmethod
    def get_random_user(cls):
        # 从枚举成员中随机选择一个
        return random.choice(list(cls))

if __name__ == '__main__':
    # 使用示例
    random_user = XbbUserEnum.get_random_user()
    print(f"随机选择的用户: {random_user.value[1]} (ID: {random_user.value[0]})")