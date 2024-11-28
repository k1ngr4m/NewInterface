# coding=utf-8
import requests

from utils.logutil import logger


class RequestSend:
    # 封装requests请求函数
    def api_run(self, url, method, data=None, headers=None, cookies=None):
        res = None
        logger.info("请求的url为\n\t{},类型为{}".format(url, type(url)))
        # logger.info("请求的method为\n\t{},类型为{}".format(method, type(method)))
        logger.info("请求的data为\n\t{},类型为{}".format(data, type(data)))
        logger.info("请求的headers为\n\t{},类型为{}".format(headers, type(headers)))
        # logger.info("请求的cookies为\n\t{},类型为{}".format(cookies, type(cookies)))
        if method == "get":
            res = requests.get(url, data=data, headers=headers, cookies=cookies)
        elif method == "post":
            if headers == {"Content-Type": "application/json"}:
                res = requests.post(url, json=data, headers=headers, cookies=cookies)
            elif headers == {"Content-Type": "application/x-www-form-urlencoded"}:
                res = requests.post(url, data=data, headers=headers, cookies=cookies)
            else:
                print(res)
                res = requests.post(url, json=data, headers=headers)
        code = res.status_code
        # cookies = res.cookies.get_dict()
        dict1 = dict()
        try:
            body = res.json()
        except:
            body = res.text
        dict1['code'] = code
        dict1['body'] = body
        # dict1['cookies'] = cookies
        return dict1

    def send(self, url, method, **kwargs):
        return self.api_run(url=url, method=method, **kwargs)
