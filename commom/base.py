# coding=utf-8
import hashlib
import json
from string import Template
import re
from config.jenkinsparam import token
from config.jenkinsparam import corpid
from config.jenkinsparam import userid
from config.jenkinsparam import login_para


# 生成请求头里的sign值
def create_sign_code(request_parameters, production_token):
    request_parameters = json.dumps(request_parameters)
    parameters = request_parameters + str(production_token)
    sign = hashlib.sha256(parameters.encode('utf-8')).hexdigest()
    return sign


def deal_login_para():
    if "userId" in login_para:
        try:
            login_para_dict = {}
            login_para_dict = eval(login_para)
            login_corpid = login_para_dict['corpid']
            login_userId = login_para_dict['userId']
            login_token = login_para_dict['xbbAccessToken']

        except Exception as e:
            print(e)


def get_data(data):
    for k, v in data.items():
        if k == 'corpid':
            if "corpid" in login_para:
                login_para_dict = eval(login_para)
                login_corpid = login_para_dict['corpid']
                data['corpid'] = login_corpid
            else:
                data['corpid'] = corpid
        if k == 'userId':
            if "userId" in login_para:
                login_para_dict = eval(login_para)
                login_userId = login_para_dict['userId']
                data['userId'] = login_userId
            else:
                data['userId'] = userid
        if type(v) == dict:
            get_data(v)
    return data


def get_headers(data, headers):
    if "xbbAccessToken" in login_para:
        login_para_dict = eval(login_para)
        login_token = login_para_dict['xbbAccessToken']
    else:
        login_token = token
    sign_code = create_sign_code(data, login_token)
    headers['sign'] = sign_code
    return headers


def find(data):
    # 判断data是否为字典
    if isinstance(data, dict):
        data = json.dumps(data)
        pattern = "\\${(.*?)}"
        ret = re.findall(pattern, data)
        return ret


# 进行参数替换
def replace(ori_data, replace_data):
    ori_data = json.dumps(ori_data)
    s = Template(ori_data)
    return s.safe_substitute(replace_data)


# 根据var，逐层获取json格式的值
def parse_relation(var, resdata):
    if not var:
        return resdata
    else:
        if type(resdata) == list:
            for i in range(len(resdata)):
                resdata = resdata[i].get(var[0])
        else:
            resdata = resdata.get(var[0])
        del var[0]
        return parse_relation(var, resdata)
    # if not var:
    #     return resdata
    # else:
    #     if type(resdata) == list:
    #         new_resdata = []
    #         for item in resdata:
    #             if isinstance(item, dict) and var[0] in item:
    #                 new_resdata.append(item[var[0]])
    #             elif isinstance(item, list):
    #                 new_item = parse_relation(var[:], item)
    #                 if new_item is not None:
    #                     new_resdata.append(new_item)
    #         resdata = new_resdata
    #     elif isinstance(resdata, dict) and var[0] in resdata:
    #         resdata = resdata[var[0]]
    #     else:
    #         resdata = None
    #     del var[0]
    #     return parse_relation(var, resdata)


def trans_str_bool(string):
    return str(string).replace("'", '"').replace('None', 'null').replace('False', 'false').replace('True', 'true')


if __name__ == '__main__':
    ori_data = {"admin-token": "${token}"}
    replace_data = {'token': 'k1ngr4m'}
    print(replace(ori_data, replace_data))
