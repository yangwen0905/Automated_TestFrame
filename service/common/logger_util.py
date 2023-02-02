import os
import logging
import time
from service.common.yaml_operate_util import  read_config_yaml
from service.conf.setting import LOG_PATH


class LoggerUtil():
    '''logging封装日志记录器'''
    def __init__(self,loggerName="log"):
        # 设置日志文件的路径和名称。以时间命名日志文件，格式为"年-月-日"
        self.log_path_and_name = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y-%m-%d")))

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

        

        
        # 创建一个logger，loggerName为该logger名字
        self.logger = logging.getLogger(loggerName)
        
        # # 创建文件和控制台日志处理器
        # self.file_handler = None
        # self.console_handlero = None
    
    def get_logger():
        pass

    def remove_handler():
        pass

logger = LoggerUtil().logger