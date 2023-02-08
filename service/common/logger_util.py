import os
import logging
import time
import json as complexjson
from service.common.yaml_operate_util import clean_loginToken_yaml, read_config_yaml
from service.data.setting import LOG_PATH


class LoggerUtil():
    '''logging封装日志记录器'''
    def __init__(self,loggerName="log"):
        # 设置日志文件的路径和名称。以时间命名日志文件，格式为"年-月-日"
        self.log_path_and_name = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y-%m-%d")))

        # 创建一个logger，loggerName为该logger名字
        self.logger = logging.getLogger(loggerName)
        self.filelogger = logging.FileHandler(self.log_path_and_name, mode='a', encoding="UTF-8")
        self.console = logging.StreamHandler()
        self.formater = logging.Formatter(
            '[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s')
        self.filelogger.setFormatter(self.formater)
        self.console.setFormatter(self.formater)
        self.logger.addHandler(self.filelogger)
        self.logger.addHandler(self.console)
        # 设置日志级别为DEBUG
        self.logger.setLevel(logging.DEBUG)
        self.console.setLevel(logging.DEBUG)
        self.filelogger.setLevel(logging.DEBUG)

    def setup_class(self):
        # # 生成日志类对象
        # self.loggerutil = LoggerUtil()
        # # 获得日志对象
        # self.logger = self.loggerutil.get_logger()
        # # 获得接口请求对象
        # self.httpRequest = RequestUtil(self.logger)
        # 清空loginToken.yaml文件中提取的值
        clean_loginToken_yaml()
    def setup(self):
        self.logger.info("-------------接口测试用例执行开始-------------")

    def teardown(self):
        self.logger.info("-------------接口测试用例执行结束-------------")        

    def teardown_class(self):
        self.loggerutil.remove_handler()  # 移除日志处理器
        




        
        # # 创建文件和控制台日志处理器
        # self.file_handler = None
        # self.console_handlero = None
    
    def get_logger():
        pass

    def remove_handler():
        pass
    
    def request_log(url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None,
                **kwargs):
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

logger = LoggerUtil().logger