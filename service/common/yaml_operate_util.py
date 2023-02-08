import os
import yaml
from service.data.setting import BASE_PATH, CASE_DATA_PATH, CONFIG_FILE, LOGIN_TOKEN_YAML_FILE, EXTACT_FILE


# 向loginToken_yaml文件写入数据
def write_loginToken_yaml(data):
    with open(LOGIN_TOKEN_YAML_FILE, encoding="utf-8", mode="a") as f:  # a：追加
        yaml.dump(data, stream=f, allow_unicode=True)


# 向loginToken_yaml文件读取数据
def read_loginToken_yaml(goal):
    with open(LOGIN_TOKEN_YAML_FILE, encoding="utf-8", mode="r") as f:
        value = yaml.load(f.read(), Loader=yaml.FullLoader)
        goal_list = value.keys()
        if goal in goal_list:
            return value[goal]
        else:
            print('不存在该配置')


# 清空loginToken_yaml文件写入数据
def clean_loginToken_yaml():
    with open(LOGIN_TOKEN_YAML_FILE, encoding="utf-8", mode="w") as f:  # w:替换
        f.truncate()


# 读取测试用例yaml文件
def read_testcase_data_yaml(yamlpath):
    with open(CASE_DATA_PATH + "/" + yamlpath, encoding="utf-8", mode="r") as f:
        value = yaml.load(f.read(), Loader=yaml.FullLoader)
        return value


def read_config_yaml(one_key, two_key):
    with open(CONFIG_FILE, encoding="utf-8", mode="r") as f:
        cfg = yaml.load(f.read(), Loader=yaml.FullLoader)
        return cfg[one_key][two_key]


# 向extract_yaml文件读取数据
def read_extract_yaml(goal):
    with open(EXTACT_FILE, encoding="utf-8", mode="r") as f:
        value = yaml.load(f.read(), Loader=yaml.FullLoader)
        return value[goal]

# 向extract_yaml文件读取数据形成列表
def read_extract_yaml_list(goal):
    with open(EXTACT_FILE, encoding="utf-8", mode="r") as f:
        value = yaml.load(f.read(), Loader=yaml.FullLoader)
        print(value)
        # for line in f.readlines():
        #     if goal in line:
        #         value = yaml.load(line.read(), Loader=yaml.FullLoader)
        #         print(value)


# 向extract_yaml文件写入数据
def write_extract_yaml(data):
    with open(EXTACT_FILE, encoding="utf-8", mode="a") as f:  # a：追加
        yaml.dump(data, stream=f, allow_unicode=True)

# 此文件随着项目需求可能封装项目中需要用到的公共方法
# 如
# MD5加密
# 生成时间字符串
# 生成随机号码
