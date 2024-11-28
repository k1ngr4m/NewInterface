"""
自动创建测试用例
"""
import commom.osbase as osbase
# -*- coding = utf-8 -*-

import json
import re

# 空字符串
str_none = ''
# 字符边界最大值
too_long_str = '豫章故郡，洪都新府。星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃之榻。雄州雾列，俊采星驰。台隍枕夷夏之交，宾主尽东南之美。都督阎公之雅望，棨戟遥临；宇文新州之懿范，襜帷暂驻。十旬休假，胜友如云；千里逢迎，高朋满座。腾蛟起凤，孟学士之词宗；紫电青霜，王将军之武库。家君作宰，路出名区；童子何知，躬逢胜饯。时维九月，序属三秋。潦水尽而寒潭清，烟光凝而暮山紫。俨骖騑于上路，访风景于崇阿；临帝子之长洲，得天人之旧馆。层峦耸翠，上出重霄；飞阁流丹，下临无地。鹤汀凫渚，穷岛屿之萦回；桂殿兰宫，即冈峦之体势。披绣闼，俯雕甍，山原旷其盈视，川泽纡其骇瞩。闾阎扑地，钟鸣鼎食之家；舸舰弥津，青雀黄龙之舳。云销雨霁，彩彻区明。落霞与孤鹜齐飞，秋水共长天一色。渔舟唱晚，响穷彭蠡之滨；雁阵惊寒，声断衡阳之浦。遥襟甫畅，逸兴遄飞。爽籁发而清风生，纤歌凝而白云遏。睢园绿竹，气凌彭泽之樽；邺水朱华，光照临川之笔。四美具，二难并。穷睇眄于中天，极娱游于暇日。天高地迥，觉宇宙之无穷；兴尽悲来，识盈虚之有数。望长安于日下，目吴会于云间。地势极而南溟深，天柱高而北辰远。关山难越，谁悲失路之人？萍水相逢，尽是他乡之客。怀帝阍而不见，奉宣室以何年？嗟乎！时运不齐，命途多舛。冯唐易老，李广难封。屈贾谊于长沙，非无圣主；窜梁鸿于海曲，岂乏明时？所赖君子见机，达人知命。老当益壮，宁移白首之心？穷且益坚，不坠青云之志。酌贪泉而觉爽，处涸辙以犹欢。北海虽赊，扶摇可接；东隅已逝，桑榆非晚。孟尝高洁，空余报国之情；阮籍猖狂，岂效穷途之哭！勃，三尺微命，一介书生。无路请缨，等终军之弱冠；有怀投笔，慕宗悫之长风。舍簪笏于百龄，奉晨昏于万里。非谢家之宝树，接孟氏之芳邻。他日趋庭，叨陪鲤对；今兹捧袂，喜托龙门。杨意不逢，抚凌云而自惜；钟期既遇，奏流水以何惭？呜乎！胜地不常，盛筵难再；兰亭已矣，梓泽丘墟。临别赠言，幸承恩于伟饯；登高作赋，是所望于群公。敢竭鄙怀，恭疏短引；一言均赋，四韵俱成。请洒潘江，各倾陆海云尔：滕王高阁临江渚，佩玉鸣鸾罢歌舞。画栋朝飞南浦云，珠帘暮卷西山雨。闲云潭影日悠悠，物换星移几度秋。阁中帝子今何在？槛外长江空自流。'
# max_int = 2147483647
# min_int = -2147483648
max_int = 99999
min_int = -99
# 特殊字符
content_special_str = '~!@#$%^&*_-+<>?:()[]{}|/?.'
positive_case_file = r'utils/data/positive_case.json'
negative_case_file = r"utils/data/negative_case.json"
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

    def create_negative_case(self):
        self.create_case()

    # API接口用例自动生成规则
    def create_case(self):
        # 没有用例文件则创建
        osbase.create_file(negative_case_file)
        # 写入前清空
        osbase.truncate_file(negative_case_file)
        # 读取原用例
        init_case_list = osbase.get_case_list(positive_case_file)

        new_case_list = []
        for i in range(len(init_case_list)):
            # 读取单条用例
            init_case_dict = init_case_list[i]
            new_case_data = self.replace_para(init_case_dict)
            new_case_list = new_case_list + new_case_data
        osbase.write_file(negative_case_file, new_case_list)

    def replace_para(self, init_dict):
        new_case_list = []

        normal_para = self.replace_nothing(init_dict)
        new_case_list.append(normal_para)

        init_para = init_dict['req_body']
        init_title = init_dict['title']
        # 遍历请求参数
        for para_key in init_para.keys():
            if para_key != "userId" and para_key != "corpid" and para_key != "platform" and para_key != "frontDev":
                # 规则1：构造key缺失的用例
                mode = 'none'
                lose_key_case_name = f"{str(init_title)}中{para_key}的key缺失"
                key_to_none_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                new_case_list.append(key_to_none_para_list)

                # 规则2: 构造value缺失的用例
                mode = 'value_none'
                lose_key_case_name = f"{str(init_title)}中{para_key}的value缺失"
                int_to_max_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                new_case_list.append(int_to_max_para_list)

                # 规则3: 数字类型value值转变为最大int值
                mode = 'max'
                lose_key_case_name = f"{str(init_title)}中{para_key}的数字类型value值转变为最大int值"
                int_to_max_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                if int_to_max_para_list is not None:
                    new_case_list.append(int_to_max_para_list)

                # 规则4: 数字类型value值转变为最小int值
                mode = 'min'
                lose_key_case_name = f"{str(init_title)}中{para_key}的数字类型value值转变为最小int值"
                int_to_min_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                if int_to_min_para_list is not None:
                    new_case_list.append(int_to_min_para_list)

                # 规则5: 字符类型最大可允许输入长度验证
                mode = 'long_str'
                lose_key_case_name = f"{str(init_title)}中{para_key}的字符串类型value值过长"
                too_long_str_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                if too_long_str_para_list is not None:
                    new_case_list.append(too_long_str_para_list)

                # 规则6：将int转换为list
                mode = 'int_to_list'
                lose_key_case_name = f"{str(init_title)}中{para_key}的数字类型value值转变为list格式"
                int_to_list_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                if int_to_list_para_list is not None:
                    new_case_list.append(int_to_list_para_list)

                # 规则7：构造参数格式异常的用例, 将str转换为list
                mode = 'str_to_list'
                lose_key_case_name = f"{str(init_title)}中{para_key}的字符串类型value值转变为list格式"
                str_to_list_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                if str_to_list_para_list is not None:
                    new_case_list.append(str_to_list_para_list)

                # 规则8：int型包含特殊字符
                mode = 'int_to_special'
                lose_key_case_name = f"{str(init_title)}中{para_key}的int型value包含特殊字符"
                int_to_special_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                if int_to_special_para_list is not None:
                    new_case_list.append(int_to_special_para_list)

                # 规则9：的str型value包含特殊字符
                mode = 'str_to_special'
                lose_key_case_name = f"{str(init_title)}中{para_key}的str型value包含特殊字符"
                str_to_special_para_list = self.replace_value(mode, init_dict, para_key, lose_key_case_name, '100002')
                if str_to_special_para_list is not None:
                    new_case_list.append(str_to_special_para_list)

        return new_case_list

    # 正常入参
    def replace_nothing(self, init_dict):
        init_title = init_dict['title']
        lose_key_case_name = f"{init_title}正常入参"
        self.id = self.id + 1

        temp_case_data = init_dict
        temp_para = init_dict['req_body']

        temp_case_data['id'] = self.id
        temp_case_data['title'] = lose_key_case_name
        temp_case_data['req_body'] = temp_para
        temp_case_data['expected_code'] = '1'
        return temp_case_data

    def replace_value(self, mode, init_dict, para_key, lose_key_case_name, expected_code):
        ischanged = False

        temp_case_data = {}
        temp_para = dict.copy(init_dict['req_body'])

        if mode == 'none':
            temp_para[str_none] = temp_para.pop(para_key)
            ischanged = True

        elif mode == 'value_none':
            temp_para[para_key] = str_none
            ischanged = True

        elif isinstance(temp_para[para_key], int):
            ischanged = True
            if mode == 'max':
                temp_para[para_key] = max_int
            elif mode == 'min':
                temp_para[para_key] = min_int
            elif mode == 'int_to_list':
                list_type = []
                list_type.insert(0, temp_para[para_key])
                temp_para[para_key] = list_type
            elif mode == 'int_to_special':
                temp_para[para_key] = content_special_str
            else:
                ischanged = False

        elif isinstance(temp_para[para_key], str):
            ischanged = True
            if mode == 'long_str':
                temp_para[para_key] = too_long_str
            elif mode == 'str_to_list':
                list_type = []
                list_type.insert(0, temp_para[para_key])
                temp_para[para_key] = list_type
            elif mode == 'str_to_special':
                temp_para[para_key] = content_special_str
            else:
                ischanged = False

        if ischanged:
            self.id = self.id + 1
            temp_case_data['id'] = self.id
            temp_case_data['title'] = lose_key_case_name
            temp_case_data['method'] = init_dict['method']
            temp_case_data['path'] = init_dict['path']
            temp_case_data['req_body'] = temp_para
            temp_case_data['relation'] = ''
            temp_case_data['isdel'] = 1
            temp_case_data['expected_code'] = expected_code
            return temp_case_data


'''

        # 规则3：将dict转换为list
        temp_param = dict.copy(init_param)
        if isinstance(temp_param[param_key], dict):
            # 第二层 key:value处理
            init_second_level_dict_data = dict(init_param[param_key])

            # 遍历第二层dict格式的数据
            for second_level_key in init_second_level_dict_data.keys():
                temp_param = dict.copy(init_param)
                temp_second_level_dict = dict.copy(init_second_level_dict_data)
                # 构造第二层dict数据的key缺失用例
                temp_second_level_dict[str_none] = temp_second_level_dict.pop(second_level_key)
                temp_param[param_key] = temp_second_level_dict
                matchers = create_case_pattern.findall(str(temp_param))
                for matcher in matchers:
                    temp_param = str(temp_param).replace(str(matcher), str('\"')).replace('None',
                                                                                          'null').replace(
                        'False', 'false').replace('True', 'true')
                case_data['request_param'] = json.loads(temp_param)
                second_dict_key_lose = str(api_name) + "中子级dict参数的key" + second_level_key + "缺失"
                case_data['case_name'] = second_dict_key_lose
                # 写入自动化用例文件
                with open(auto_case_file, mode='a+', encoding='utf-8') as case_write:
                    case_write.write(str(case_data) + "\n")

                # 构造第二层dict数据的value值缺失用例
                temp_param = dict.copy(init_param)
                temp_second_level_dict = dict.copy(init_second_level_dict_data)
                temp_second_level_dict[second_level_key] = str_none
                temp_param[param_key] = temp_second_level_dict
                matchers = create_case_pattern.findall(str(temp_param))
                for matcher in matchers:
                    temp_param = str(temp_param).replace(str(matcher), str('\"')).replace('None',
                                                                                          'null').replace(
                        'False', 'false').replace('True', 'true')
                case_data['request_param'] = json.loads(temp_param)
                second_dict_value_lose = str(api_name) + "中子级dict参数" + second_level_key + "的value缺失"
                case_data['case_name'] = second_dict_value_lose
                # 写入自动化用例文件
                with open(auto_case_file, mode='a+', encoding='utf-8') as case_write:
                    case_write.write(str(case_data) + "\n")

                # 构造第二层dict数据的int最大值
                temp_param = dict.copy(init_param)
                temp_second_level_dict = dict.copy(init_second_level_dict_data)
                if isinstance(temp_second_level_dict[second_level_key], int):
                    temp_second_level_dict[second_level_key] = max_int
                    temp_param[param_key] = temp_second_level_dict
                    matchers = create_case_pattern.findall(str(temp_param))
                    for matcher in matchers:
                        temp_param = str(temp_param).replace(str(matcher), str('\"')).replace('None',
                                                                                              'null').replace(
                            'False', 'false').replace('True', 'true')
                    case_data['request_param'] = json.loads(temp_param)
                    second_dict_max_int_judge = str(
                        api_name) + "中子级dict中" + second_level_key + "的int型值为最大整型"
                    case_data['case_name'] = second_dict_max_int_judge
                    # 写入自动化用例文件
                    with open(auto_case_file, mode='a+', encoding='utf-8') as case_write:
                        case_write.write(str(case_data) + "\n")

                # 构造第二层dict数据的int最小值
                temp_param = dict.copy(init_param)
                temp_second_level_dict = dict.copy(init_second_level_dict_data)
                if isinstance(temp_second_level_dict[second_level_key], int):
                    temp_second_level_dict[second_level_key] = min_int
                    temp_param[param_key] = temp_second_level_dict
                    matchers = create_case_pattern.findall(str(temp_param))
                    for matcher in matchers:
                        temp_param = str(temp_param).replace(str(matcher), str('\"')).replace('None',
                                                                                              'null').replace(
                            'False', 'false').replace('True', 'true')
                    case_data['request_param'] = json.loads(temp_param)
                    second_dict_min_int_judge = str(
                        api_name) + "中子级dict中" + second_level_key + "的int型值为最小整型"
                    case_data['case_name'] = second_dict_min_int_judge
                    # 写入自动化用例文件
                    with open(auto_case_file, mode='a+', encoding='utf-8') as case_write:
                        case_write.write(str(case_data) + "\n")

                # 构造第二层dict数据int改为特殊字符
                temp_param = dict.copy(init_param)
                temp_second_level_dict = dict.copy(init_second_level_dict_data)
                if isinstance(temp_second_level_dict[second_level_key], int):
                    temp_second_level_dict[second_level_key] = content_special_str
                    matchers = create_case_pattern.findall(str(temp_param))
                    temp_param[param_key] = temp_second_level_dict
                    for matcher in matchers:
                        temp_param = str(temp_param).replace(str(matcher), str('\"')).replace('None',
                                                                                              'null').replace(
                            'False', 'false').replace('True', 'true')
                    case_data['request_param'] = json.loads(temp_param)
                    second_dict_special_char_judge = str(
                        api_name) + "中子级dict中" + second_level_key + "的int型值包含特殊字符"
                    case_data['case_name'] = second_dict_special_char_judge
                    # 写入自动化用例文件
                    with open(auto_case_file, mode='a+', encoding='utf-8') as case_write:
                        case_write.write(str(case_data) + "\n")

                # 构造第二层dict数据字符串包含特殊字符
                temp_param = dict.copy(init_param)
                temp_second_level_dict = dict.copy(init_second_level_dict_data)
                if isinstance(temp_second_level_dict[second_level_key], str):
                    temp_second_level_dict[second_level_key] = content_special_str
                    temp_param[param_key] = temp_second_level_dict
                    matchers = create_case_pattern.findall(str(temp_param))
                    for matcher in matchers:
                        temp_param = str(temp_param).replace(str(matcher), str('\"')).replace('None',
                                                                                              'null').replace(
                            'False', 'false').replace('True', 'true')
                    case_data['request_param'] = json.loads(temp_param)
                    second_dict_special_char_judge = str(
                        api_name) + "中子级dict中" + second_level_key + "的str型值包含特殊字符"
                    case_data['case_name'] = second_dict_special_char_judge
                    # 写入自动化用例文件
                    with open(auto_case_file, mode='a+', encoding='utf-8') as case_write:
                        case_write.write(str(case_data) + "\n")

                # 构造第二层dict数据str型值的最大长度(样例为滕王阁序全文)
                temp_param = dict.copy(init_param)
                temp_second_level_dict = dict.copy(init_second_level_dict_data)
                if isinstance(temp_second_level_dict[second_level_key], str):
                    temp_second_level_dict[second_level_key] = too_long_str
                    temp_param[param_key] = temp_second_level_dict
                    matchers = create_case_pattern.findall(str(temp_param))
                    for matcher in matchers:
                        temp_param = str(temp_param).replace(str(matcher), str('\"')).replace('None',
                                                                                              'null').replace(
                            'False', 'false').replace('True', 'true')
                    case_data['request_param'] = json.loads(temp_param)
                    second_dict_special_char_judge = str(
                        api_name) + "中子级dict中" + second_level_key + "的str型最大值"
                    case_data['case_name'] = second_dict_special_char_judge
                    # 写入自动化用例文件
                    with open(auto_case_file, mode='a+', encoding='utf-8') as case_write:
                        case_write.write(str(case_data) + "\n")
'''
if __name__ == '__main__':
    cr = CreateCase()
    cr.create_negative_case()
