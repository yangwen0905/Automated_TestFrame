import requests
import json as complexjson
from service.common.yaml_operate_util import read_config_yaml, read_extract_yaml
from service.common.logger_util import logger

class RequestUtil():

    session = requests.session()

    def __init__(self):
        #获得日志对象
        # self.logger = logger
        #初始化基本路径
        self.auth_base_url = read_config_yaml('url', 'auth_base_url')
        #初始化基本路径
        self.base_url = read_config_yaml('url', 'base_url')
        #初始化请求头（如果不初始化此变量，则get,post,put,delete方法传参时会报错）
        self.last_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        #初始化请求数据（如果不初始化此变量，则get,post,put,delete方法传参时会报错）
        self.last_data = {}
    
    # 封装各类型请求
    def get(self, url, headers, data):
         res = requests.get(url, headers=headers, data=data)
         print(res.json())
         return res

    def post(self, url, headers, data):
        res = requests.post(url, headers=headers, data=data)
        return res

    def put(self, url, headers, data):
        res = requests.put(url, headers=headers, data=data)
        return res

    def delete(self, url, headers, data):
        res = requests.delete(url, headers=headers, data=data)
        return res

    def patch(self, url, headers, data):
        res = requests.put(url, headers=headers, data=data)
        return res


    #统一请求信息
    def send_token_request(self, **kwargs):
        res = RequestUtil.session.request(**kwargs)
        return res

    def send_request(self, method, url, headers, data=None, **kwargs):
        json = dict(**kwargs).get("json")
        params = dict(**kwargs).get("params")
        files = dict(**kwargs).get("files")
        cookies = dict(**kwargs).get("cookies")
        # res = RequestUtil.session.request(**kwargs)
        #method参数转换为小写
        self.last_method = str(method).lower()

        #处理请求路径url
        #如果请求路径中包括${和}，则需要做参数提取
        # for cs in range(1,str(url).count('${')+1):
        #     if '${' in url and '}' in url:
        #         startIndex = str(url).find('${')
        #         endIndex = str(url).find('}')
        #         oldValue = str(url)[int(startIndex):int(endIndex)+1]
        #         newValue = read_extract_yaml(str(oldValue)[2:-1])
        #         url = str(url).replace(oldValue, newValue)
        self.last_url = self.base_url + url

        #如果headers不为None并且为字典类型，则在self.headers中增加请求头
        # if headers and isinstance(headers, dict):
        #     for key,value in headers.items():
        #         if str(value).startswith('${') and str(value).endswith('}'):
        #             self.last_headers[str(key)] = read_extract_yaml(str(value)[2:-1])
        #         else:
        #             self.last_headers[str(key)] = str(value)
        if headers and isinstance(headers, dict):
            for key,value in headers.items():
                self.last_headers[str(key)] = str(value)
        #如果data不为None并且为字典类型，则转换成json字符串，（因为get和post方式都支持传入json）
        # if data and isinstance(data, dict):
        #     for key,value in data.items():
        #         if str(value).startswith('${') and str(value).endswith('}'):
        #             data[str(key)] = read_extract_yaml(str(value)[2:-1])
        #         else:
        #             data[str(key)] = str(value)
        # self.last_data = complexjson.dumps(data)
        self.last_data = data
        # 输出日志获取请求信息
        self.request_log(url, method, data, json,
                         params, headers, files, cookies)
        
        #根据不同请求方式调用requests模块中不同的方法
        res = ''
        if self.last_method == "get":
            res = self.get(self.last_url, self.last_headers, self.last_data)
        elif self.last_method == "post":
            res = self.post(self.last_url, self.last_headers, self.last_data)
        elif self.last_method == "PUT":
            if json:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = complexjson.dumps(json)
            res = self.put(self.last_url, self.last_headers, self.last_data)
        elif self.last_method == "DELETE":
            res = self.delete(self.last_url, self.last_headers, self.last_data)
        elif self.last_method == "PATCH":
            if json:
                data = complexjson.dumps(json)
            res = self.patch(self.last_url, self.last_headers, self.last_data)
        else:
            logger.info('不支持的接口请求方式！')
    

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None, **kwargs):
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        logger.info("接口请求头 ==>> {}".format(
            complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(
            complexjson.dumps(params, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 data 参数 ==>> {}".format(
            complexjson.dumps(data, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 json 参数 ==>> {}".format(
            complexjson.dumps(json, indent=4, ensure_ascii=False)))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        logger.info("接口 cookies 参数 ==>> {}".format(
            complexjson.dumps(cookies, indent=4, ensure_ascii=False)))


    # 断言封装
    def validate_result(self, expectResult, actualResult, status_code, logger):
        '''
        断言预期结果和实际结果是否正确
        expectResult: 期望结果
        actualResult: 实际结果
        status_code: 状态码
        logger: 日志对象
        '''

        #定义一个断言成功与否的标记，0为成功，其他为失败
        flag = 0
        #如果预期结果为一个列表类型
        if isinstance(expectResult,list):
            pass
