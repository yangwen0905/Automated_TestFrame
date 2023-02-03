import requests
import re
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
        # #初始化请求头（如果不初始化此变量，则get,post,put,delete方法传参时会报错）
        # self.last_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # #初始化请求数据（如果不初始化此变量，则get,post,put,delete方法传参时会报错）
        # self.last_data = {}
        # self.last_params = {}
        # self.obj = obj   #热加载

    def replace_value(self, data):
        if data:
            #保存数据类型
            data_type = type(data)
            #判断数据类型转换成str
            if isinstance(data, dict) or isinstance(data,list):
                str_data = complexjson.dumps(data)
            else:
                str_data = str(data)
            for cs in range(1,str_data.count('${') + 1):
                if "${" in str_data and "} "in str_data:
                    start_index = str_data.index('${')
                    end_index = str_data.index('}', start_index)
                    old_value = str_data[start_index:end_index+1]
                    print("old_value:"+old_value)
                    #反射：通过类的对象和方法字符串调用方法
                    func_name = old_value[2:old_value.index('(')]
                    args_value1 = old_value[old_value.index('(')+1:old_value.index(')')]
                    new_value = ""
                    if args_value1 != "":
                        args_value2 = args_value1.split(',')
                        new_value = getattr(self.obj, func_name)(*args_value2)
                    else:
                        new_value = getattr(self.obj, func_name)()
                    str_data = str_data.replace(old_value,str(new_value))
            #还原数据类型
            if isinstance(data,dict) or isinstance(data,list):
                data = complexjson.loads(str_data)
            else:
                data = data_type(str_data)

    #规范yaml测试用例
    def standard_yaml(self,caseinfo):
        caseinfo_keys = caseinfo.keys()
        #判断以及关键字是否包含：story，requst,validate
        if "feature" in caseinfo_keys and "story" in caseinfo_keys and "title" in caseinfo_keys and "request" in caseinfo_keys and "vilidate" in caseinfo_keys:
            request_keys = caseinfo["request"].keys()
            #判断request下面是否包含：method、url
            if "method" in request_keys and "url" in request_keys:
                logger.info("yaml基本架构检查通过")
                method = caseinfo["request"].pop("method")
                url = caseinfo["request"].pop("url")
                
                
                res = self.send_request(method, url,**caseinfo['request'])   #caseinfo需要解包加**
                return_text = res.text
                return_code = res.status_code
                return_json = ""
                print("return_text:"+return_text)
                print(return_code)
                print("return_json"+return_json)
                try:
                    return_json = res.json()
                except Exception as e:
                    logger.info("extract返回的结果不是JSON格式")
                
                #断言：
                


    
    # # 封装各类型请求
    # def get(self, method, url, **kwargs):
    #      res = RequestUtil.session.request(method, url, **kwargs)
    #      return res

    # def post(self, method, url, **kwargs):
    #     res = RequestUtil.session.request(method, url, **kwargs)
    #     # res = requests.post(method=method, url=url, **kwargs)
    #     return res

    # def put(self, method, url, **kwargs):
    #     res = RequestUtil.session.request(method, url, **kwargs)
    #     return res

    # def delete(self, method, url, **kwargs):
    #     res = RequestUtil.session.request(method, url, **kwargs)
    #     return res

    # def patch(self, method, url, **kwargs):
    #     res = RequestUtil.session.request(method, url, **kwargs)
    #     return res


    # #统一请求信息
    # def send_token_request(self, **kwargs):
    #     res = RequestUtil.session.request(**kwargs)
    #     return res

    def send_request(self, method, url, **kwargs):
        # #method参数转换为小写
        self.method = str(method).lower()
        
        if url == "token":
            self.url = self.auth_base_url + url
        else:
            self.url = self.base_url + url
        # #参数替换
        # for key, value in kwargs.items():
        #     if key in ['params','data','json','headers']:
        #         print(kwargs[key])
                
            # elif key == "files":
            #     for file_key,file_path in value.items():
            #         value[file_key] = open(file_path,'rb')
        
                   
        res = RequestUtil.session.request(method, self.url, **kwargs)
        # return res
        # 输出日志获取请求信息
        
        
        # 根据不同请求方式调用requests模块中不同的方法
        
        # if self.method == "get":
        #     res = self.get(method, self.url, **kwargs)
        # elif self.method == "post":
        #     res = self.post(method, self.url, **kwargs)
        # elif self.last_method == "put":
        #     res = self.put(method, self.url, **kwargs)
        # elif self.last_method == "delete":
        #     res = self.delete(method, self.url, **kwargs)
        # elif self.last_method == "patch":
        #     res = self.patch(method, self.url, **kwargs)
        # else:
        #     logger.info('不支持的接口请求方式！')
        self.request_log(url, method, **kwargs)
        return res
    
    

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
