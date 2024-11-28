# coding=utf-8
import time

from commom import base
from utils.logutil import logger
from utils.readmysql import RdTestcase
from utils.requestsutil import RequestSend

case_data = RdTestcase()

title = ''
environment = 'test1'
path = '/pro/v1/form/data/add?lang=zh_CN'
# request_body = \
# '{"corpid":"ding66041eb1c6df73f535c2f4657eb6378f","userId":"215252650523902241","platform":"web","businessType":21500,"dataIdList":[132]}'
res_data = None
conf_key = case_data.loadConfkey('xbb', environment)
url = conf_key['value'] + path
headers = eval(conf_key['headers'])
method = 'post'
# data = eval(request_body)
case_name = title

# data = base.get_data(data)
# headers = base.get_headers(data, headers)

try:
    for i in range(6, 48):
        # logger.info("正在执行{}用例".format(case_name))
        request_body = \
            '{"corpid":"ding0064986624e3b83b35c2f4657eb6378f","userId":"215252650523902241","platform":"web","appId":0,"menuId":0,"saasMark":1,"formId":10866,"businessType":21500,"dataId":None,"dataList":{"text_1":"再新建一个子任务'+f'{i}'+'","ownerId":[{"id":"01513441002923510676","name":"小梅航"}],"text_3":{"taskMemoText":"","taskMemoImages":[],"taskMemoLink":[],"atUserIdList":[]},"text_4":{"text":"无提醒","value":"1","color":"#646566"},"text_7":[151]},"serialNo":"","ownerId":[{"id":"01513441002923510676","name":"小梅航"}]}'
        data = eval(request_body)
        data = base.get_data(data)
        headers = base.get_headers(data, headers)
        res_data = RequestSend().send(url, method, data=data, headers=headers)
        # print(i + res_data)
        logger.info("用例执行成功，请求的结果为\n\t{}".format(res_data))
        time.sleep(10)
except:
    logger.info("用例执行失败，请查看日志。")
