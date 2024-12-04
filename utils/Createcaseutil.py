"""
自动创建测试用例
"""
import common.OSBase as osbase
# -*- coding = utf-8 -*-

import json
import re
from utils.Logutil import logger

'''
自动生成接口用例，规则如下：
1：请求参数中value缺失
2：请求参数中value格式list和dict变更
3：请求参数中int,string类型的边界值
4: 请求参数中str包含特殊字符
5: 请求参数中int变更为特殊字符
'''


class CreateCase:
    def __init__(self):
        self.id = 0
        # 定义特殊字符、空字符串、最大最小整数值等常量
        self.content_special_str = '~!@#$%^&*_-+<>?:()[]{}|/?.'
        self.str_none = ''
        self.max_int = 2147483647
        self.min_int = -2147483648
        self.too_long_str = '豫章故郡，洪都新府。星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃之榻。雄州雾列，俊采星驰。台隍枕夷夏之交，宾主尽东南之美。都督阎公之雅望，棨戟遥临；宇文新州之懿范，襜帷暂驻。十旬休假，胜友如云；千里逢迎，高朋满座。腾蛟起凤，孟学士之词宗；紫电青霜，王将军之武库。家君作宰，路出名区；童子何知，躬逢胜饯。时维九月，序属三秋。潦水尽而寒潭清，烟光凝而暮山紫。俨骖騑于上路，访风景于崇阿；临帝子之长洲，得天人之旧馆。层峦耸翠，上出重霄；飞阁流丹，下临无地。鹤汀凫渚，穷岛屿之萦回；桂殿兰宫，即冈峦之体势。披绣闼，俯雕甍，山原旷其盈视，川泽纡其骇瞩。闾阎扑地，钟鸣鼎食之家；舸舰弥津，青雀黄龙之舳。云销雨霁，彩彻区明。落霞与孤鹜齐飞，秋水共长天一色。渔舟唱晚，响穷彭蠡之滨；雁阵惊寒，声断衡阳之浦。遥襟甫畅，逸兴遄飞。爽籁发而清风生，纤歌凝而白云遏。睢园绿竹，气凌彭泽之樽；邺水朱华，光照临川之笔。四美具，二难并。穷睇眄于中天，极娱游于暇日。天高地迥，觉宇宙之无穷；兴尽悲来，识盈虚之有数。望长安于日下，目吴会于云间。地势极而南溟深，天柱高而北辰远。关山难越，谁悲失路之人？萍水相逢，尽是他乡之客。怀帝阍而不见，奉宣室以何年？嗟乎！时运不齐，命途多舛。冯唐易老，李广难封。屈贾谊于长沙，非无圣主；窜梁鸿于海曲，岂乏明时？所赖君子见机，达人知命。老当益壮，宁移白首之心？穷且益坚，不坠青云之志。酌贪泉而觉爽，处涸辙以犹欢。北海虽赊，扶摇可接；东隅已逝，桑榆非晚。孟尝高洁，空余报国之情；阮籍猖狂，岂效穷途之哭！勃，三尺微命，一介书生。无路请缨，等终军之弱冠；有怀投笔，慕宗悫之长风。舍簪笏于百龄，奉晨昏于万里。非谢家之宝树，接孟氏之芳邻。他日趋庭，叨陪鲤对；今兹捧袂，喜托龙门。杨意不逢，抚凌云而自惜；钟期既遇，奏流水以何惭？呜乎！胜地不常，盛筵难再；兰亭已矣，梓泽丘墟。临别赠言，幸承恩于伟饯；登高作赋，是所望于群公。敢竭鄙怀，恭疏短引；一言均赋，四韵俱成。请洒潘江，各倾陆海云尔：滕王高阁临江渚，佩玉鸣鸾罢歌舞。画栋朝飞南浦云，珠帘暮卷西山雨。闲云潭影日悠悠，物换星移几度秋。阁中帝子今何在？槛外长江空自流。'
        self.positive_case_file = r'utils/data/positive_case.json'
        self.negative_case_file = r"utils/data/negative_case.json"

    def create_negative_case(self):
        """创建负向测试用例"""
        self.create_case()

    def create_case(self):
        """API接口用例自动生成规则"""
        # 如果没有用例文件则创建，并在写入前清空文件内容
        osbase.create_file(self.negative_case_file)
        osbase.truncate_file(self.negative_case_file)

        # 读取原始正向用例列表
        init_case_list = osbase.get_case_list(self.positive_case_file)

        new_case_list = []
        for init_case_dict in init_case_list:
            # 生成并添加正常参数的用例
            new_case_list.append(self.replace_nothing(init_case_dict))

            # 对每个请求参数进行替换操作，生成异常用例
            new_case_list.extend(self.replace_para(init_case_dict))

        # 将新生成的用例写入到负向用例文件中
        osbase.write_file(self.negative_case_file, new_case_list)

    def replace_para(self, init_dict):
        """根据不同的规则对参数进行替换，生成新的用例"""
        new_case_list = []

        # 获取请求体和标题
        init_para = init_dict['req_body']
        init_title = init_dict['title']

        for para_key in init_para.keys():
            if para_key not in {"userId", "corpid", "platform", "frontDev"}:
                modes = [
                    ('none', f"{init_title}中{para_key}的key缺失"),
                    ('value_none', f"{init_title}中{para_key}的value缺失"),
                    ('max', f"{init_title}中{para_key}的数字类型value值转变为最大int值"),
                    ('min', f"{init_title}中{para_key}的数字类型value值转变为最小int值"),
                    ('long_str', f"{init_title}中{para_key}的字符串类型value值过长"),
                    ('int_to_list', f"{init_title}中{para_key}的数字类型value值转变为list格式"),
                    ('str_to_list', f"{init_title}中{para_key}的字符串类型value值转变为list格式"),
                    ('int_to_special', f"{init_title}中{para_key}的int型value包含特殊字符"),
                    ('str_to_special', f"{init_title}中{para_key}的str型value包含特殊字符")
                ]

                for mode, case_name in modes:
                    modified_case = self.replace_value_with_mode(mode, init_dict, para_key, case_name, '100002')
                    if modified_case:
                        new_case_list.append(modified_case)

        return new_case_list

    def replace_nothing(self, init_dict):
        """生成正常参数的用例"""
        self.id += 1
        return {
            'id': self.id,
            'title': f"{init_dict['title']}正常入参",
            'method': init_dict['method'],
            'path': init_dict['path'],
            'req_body': dict.copy(init_dict['req_body']),
            'relation': '',
            'isdel': 1,
            'expected_code': '1'
        }

    def replace_value_with_mode(self, mode, init_dict, para_key, case_name, expected_code):
        """根据指定模式替换参数值，返回修改后的用例"""
        temp_para = dict.copy(init_dict['req_body'])

        if mode == 'none':
            temp_para.pop(para_key, None)  # 移除键
        elif mode == 'value_none':
            temp_para[para_key] = self.str_none
        elif isinstance(temp_para[para_key], int):
            if mode == 'max':
                temp_para[para_key] = self.max_int
            elif mode == 'min':
                temp_para[para_key] = self.min_int
            elif mode == 'int_to_list':
                temp_para[para_key] = [temp_para[para_key]]
            elif mode == 'int_to_special':
                temp_para[para_key] = self.content_special_str
        elif isinstance(temp_para[para_key], str):
            if mode == 'long_str':
                temp_para[para_key] = self.too_long_str
            elif mode == 'str_to_list':
                temp_para[para_key] = [temp_para[para_key]]
            elif mode == 'str_to_special':
                temp_para[para_key] = self.content_special_str

        if temp_para != init_dict['req_body']:
            self.id += 1
            return {
                'id': self.id,
                'title': case_name,
                'method': init_dict['method'],
                'path': init_dict['path'],
                'req_body': temp_para,
                'relation': '',
                'isdel': 1,
                'expected_code': expected_code
            }
        return None

    def generate_test_cases(self, init_param, param_key, api_name, auto_case_file, create_case_pattern):
        if not isinstance(init_param.get(param_key), dict):
            return

        # 创建一个临时参数副本用于修改
        temp_param = init_param.copy()
        second_level_dict = init_param[param_key].copy()

        def write_case(case_data, case_name):
            """辅助函数：写入个案到文件"""
            with open(auto_case_file, mode='a+', encoding='utf-8') as case_write:
                case_write.write(json.dumps(case_data, ensure_ascii=False) + "\n")
            logger.info(f"Case written: {case_name}")

        def prepare_case(temp_param, case_name):
            """辅助函数：准备并写入个案"""
            matchers = create_case_pattern.findall(str(temp_param))
            for matcher in matchers:
                temp_param_str = str(temp_param).replace(str(matcher), str('\"')).replace('None', 'null').replace(
                    'False', 'false').replace('True', 'true')
            try:
                case_data = {
                    'request_param': json.loads(temp_param_str),
                    'case_name': f"{api_name}中{case_name}"
                }
                write_case(case_data, case_name)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON for case {case_name}: {e}")

        for second_level_key, second_level_value in second_level_dict.items():
            # 构造第二层dict数据的key缺失用例
            modified_param = temp_param.copy()
            modified_param[param_key] = second_level_dict.copy()
            modified_param[param_key][self.str_none] = modified_param[param_key].pop(second_level_key)
            prepare_case(modified_param, f"子级dict参数的key {second_level_key} 缺失")

            # 构造第二层dict数据的value值缺失用例
            modified_param = temp_param.copy()
            modified_param[param_key] = second_level_dict.copy()
            modified_param[param_key][second_level_key] = self.str_none
            prepare_case(modified_param, f"子级dict参数 {second_level_key} 的value缺失")

            # 根据第二层dict数据类型构造不同类型的测试用例
            if isinstance(second_level_value, int):
                # int最大值
                modified_param = temp_param.copy()
                modified_param[param_key] = second_level_dict.copy()
                modified_param[param_key][second_level_key] = self.max_int
                prepare_case(modified_param, f"子级dict中 {second_level_key} 的int型值为最大整型")

                # int最小值
                modified_param = temp_param.copy()
                modified_param[param_key] = second_level_dict.copy()
                modified_param[param_key][second_level_key] = self.min_int
                prepare_case(modified_param, f"子级dict中 {second_level_key} 的int型值为最小整型")

                # int改为特殊字符
                modified_param = temp_param.copy()
                modified_param[param_key] = second_level_dict.copy()
                modified_param[param_key][second_level_key] = self.content_special_str
                prepare_case(modified_param, f"子级dict中 {second_level_key} 的int型值包含特殊字符")

            elif isinstance(second_level_value, str):
                # 字符串包含特殊字符
                modified_param = temp_param.copy()
                modified_param[param_key] = second_level_dict.copy()
                modified_param[param_key][second_level_key] = self.content_special_str
                prepare_case(modified_param, f"子级dict中 {second_level_key} 的str型值包含特殊字符")

                # 字符串的最大长度
                modified_param = temp_param.copy()
                modified_param[param_key] = second_level_dict.copy()
                modified_param[param_key][second_level_key] = self.too_long_str
                prepare_case(modified_param, f"子级dict中 {second_level_key} 的str型最大值")


if __name__ == '__main__':
    cr = CreateCase()
    cr.create_negative_case()
