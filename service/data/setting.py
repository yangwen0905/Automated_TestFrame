import os

'''管理文件存放路径'''

# 项目路径   d:/**/**/api_testdev/
BASE_PATH = os.path.dirname(__file__).split('service')[0]

REPORT_PATH = os.path.join(BASE_PATH, 'report')       #报告存放目录

CASE_PATH = os.path.join(BASE_PATH, 'testcases')       #测试用例目录

CASE_DATA_PATH = os.path.join(BASE_PATH, 'service/data')          #测试数据的目录

LOG_PATH = os.path.join(BASE_PATH, 'log')             #日志存放目录

CONFIG_FILE = os.path.join(BASE_PATH, 'service/data', 'config.yaml')

LOGIN_TOKEN_YAML_FILE = os.path.join(BASE_PATH, 'service/data', 'loginToken.yaml')

EXTACT_FILE = os.path.join(BASE_PATH, 'service/data', 'extract.yaml')






if __name__ == '__main__':
    print(BASE_PATH)