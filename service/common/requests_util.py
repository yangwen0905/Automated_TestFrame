import requests
import json as complexjson
from service.common.yaml_analysis_util import YamlAnalysis
from service.common.yaml_operate_util import read_loginToken_yaml, read_config_yaml, clean_loginToken_yaml, \
    write_loginToken_yaml, read_extract_yaml, write_extract_yaml
from service.common.logger_util import LoggerUtil, logger
from service.common.validate_util import Validate





class RequestUtil():
    session = requests.session()

    def __init__(self):
        # 获得日志对象
        self.logger = logger
        # 初始化基本路径
        self.auth_base_url = read_config_yaml('url', 'auth_base_url')
        # 初始化基本路径
        self.base_url = read_config_yaml('url', 'base_url')

        # self.obj = obj   #热加载


    def send_request(self, caseinfo):
        # 请求参数解析
        last_caseinfo = YamlAnalysis.standard_yaml(self, caseinfo)
        method = last_caseinfo["method"]
        url = last_caseinfo["url"]
        kwargs = last_caseinfo['request']

        # 输出日志获取请求信息
        LoggerUtil.request_log(method, url, **kwargs)

        if method == "get" or method == "post" or method == "put" or method == "delete" or method == "patch":
            res = RequestUtil.session.request(method, url, **kwargs)
        else:
            logger.info('不支持的接口请求方式！')
        
        return res

        
        

    
