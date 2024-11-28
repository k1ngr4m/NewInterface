import os

name = os.name


# 按间距中的绿色按钮以运行脚本。
def deal_dict(data):
    for k, v in data.items():
        if k == 'corpid':
            data['corpid'] = ''
        elif k == 'userId':
            data['userId'] = ''
        elif k == 'appId':
            data['appId'] = '${appId_name}'
        elif k == 'menuId':
            data['menuId'] = '${menuId_name}'
        elif k == 'formId':
            data['formId'] = '${formId_name}'
        elif k == 'dataId':
            data['dataId'] = '${dataId_name}'
        if type(v) == dict:
            deal_dict(v)
        elif type(v) == list:
            for i in range(len(v)):
                if type(v[i]) == dict:
                    print(v[i].items)
                    deal_dict(v[i])
    return data


if __name__ == '__main__':
    strs = \
            '{"corpid":"ding66041eb1c6df73f535c2f4657eb6378f","userId":"215252650523902241","platform":"web","dataIdList":[46224696],"appId":575390,"menuId":7170276,"formId":7472084,"saasMark":2,"distributorMark":0,"businessType":0}'
    strs = strs.replace("true", "True").replace("false", "False").replace("null", "None")
    data = eval(strs)
    data = deal_dict(data)
    data = str(data).replace("", '')
    print(data)