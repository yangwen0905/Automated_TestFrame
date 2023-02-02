from common.logger_util import LoggerUtil
from common.requests_util import RequestUtil
from common.yaml_operate_util import clean_extract_yaml

class BaseUtil():
    def setup_class(self):
        # 生成日志类对象
        self.loggerutil = LoggerUtil()
        # 获得日志对象
        self.logger = self.loggerutil.get_logger()
        # 获得接口请求对象
        self.httpRequest = RequestUtil(self.logger)
        # 清空extract.yaml文件中提取的值
        clean_extract_yaml()

    
    def setup(self):
        self.logger.info("-------------接口测试用例执行开始-------------")
    
    def teardown(self):
        self.logger.info("-------------接口测试用例执行结束-------------")

    
    def teardown_class(self):
        self.loggerutil.remove_handler()    #移除日志处理器