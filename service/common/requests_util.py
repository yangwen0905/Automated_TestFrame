import jsonpath
import requests
import re
import json as complexjson
from service.common.yaml_operate_util import read_loginToken_yaml, read_config_yaml, clean_loginToken_yaml, \
    write_loginToken_yaml, read_extract_yaml, write_extract_yaml
from service.common.logger_util import logger


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


class RequestUtil():
    session = requests.session()

    def __init__(self):
        # 获得日志对象
        # self.logger = logger
        # 初始化基本路径
        self.auth_base_url = read_config_yaml('url', 'auth_base_url')
        # 初始化基本路径
        self.base_url = read_config_yaml('url', 'base_url')
        # #初始化请求头（如果不初始化此变量，则get,post,put,delete方法传参时会报错）
        # self.last_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # #初始化请求数据（如果不初始化此变量，则get,post,put,delete方法传参时会报错）
        # self.last_data = {}
        # self.last_params = {}
        # self.obj = obj   #热加载

    def replace_value(self, data):
        if data:
            # 保存数据类型
            data_type = type(data)
            # 判断数据类型转换成str
            if isinstance(data, dict) or isinstance(data, list):
                str_data = complexjson.dumps(data)
            else:
                str_data = str(data)
            for cs in range(1, str_data.count('${') + 1):
                if "${" in str_data and "} " in str_data:
                    start_index = str_data.index('${')
                    end_index = str_data.index('}', start_index)
                    old_value = str_data[start_index:end_index + 1]
                    print("old_value:" + old_value)
                    # 反射：通过类的对象和方法字符串调用方法
                    func_name = old_value[2:old_value.index('(')]
                    args_value1 = old_value[old_value.index('(') + 1:old_value.index(')')]
                    new_value = ""
                    if args_value1 != "":
                        args_value2 = args_value1.split(',')
                        new_value = getattr(self.obj, func_name)(*args_value2)
                    else:
                        new_value = getattr(self.obj, func_name)()
                    str_data = str_data.replace(old_value, str(new_value))
            # 还原数据类型
            if isinstance(data, dict) or isinstance(data, list):
                data = complexjson.loads(str_data)
            else:
                data = data_type(str_data)
            return data

    # 规范yaml测试用例
    def standard_yaml(self, caseinfo):
        caseinfo_keys = caseinfo.keys()
        # 判断以及关键字是否包含：story，request,validate
        if "feature" in caseinfo_keys and "story" in caseinfo_keys and "title" in caseinfo_keys \
                and "request" in caseinfo_keys and "validate" in caseinfo_keys:
            request_keys = caseinfo["request"].keys()
            # 判断request下面是否包含：method、url
            if "method" in request_keys and "url" in request_keys:
                logger.info("yaml基本架构检查通过")
                method = caseinfo["request"].pop("method")
                url = caseinfo["request"].pop("url")
                if url != "token":
                    headers = caseinfo["request"]["headers"]
                    headers["Authorization"] = "Bearer " + read_loginToken_yaml("Authorization")

                res = self.send_request(method, url, **caseinfo['request'])  # caseinfo需要解包加**
                return_text = res.text
                return_code = res.status_code
                return_json = ""
                try:
                    return_json = res.json()
                except Exception as e:
                    logger.info("extract返回的结果不是JSON格式")
                # 断言：

                # 判断是否成功登录，若成功，则把token值存入loginToken.yaml
                # token时效性20分钟
                if "access_token" in dict(return_json).keys():
                    clean_loginToken_yaml()
                    write_loginToken_yaml({"Authorization": return_json["access_token"]})

                # 判断是否有数据，若有，则把“我的任务组”的id存入extract.yaml
                if "data" in dict(return_json).keys():
                    return_json_data = return_json["data"]
                    for item_dict in return_json_data:
                        if "taskGroupName" in item_dict and item_dict["taskGroupName"] == "我的任务组":
                            write_extract_yaml({"taskGroupId": item_dict["taskGroupId"]})
                self.validate_result(caseinfo["validate"], return_json, return_code)
            else:
                logger.info("request中必须包含method, url")
        else:
            logger.info("一级关键字必须包含feature, story, title")

    def send_request(self, method, url, **kwargs):
        # #method参数转换为小写
        global res
        self.method = str(method).lower()

        if url == "token":
            self.url = self.auth_base_url + url
        else:
            self.url = self.base_url + url
            # 参数替换
            for key, value in kwargs.items():
                if key == 'params':
                    params = kwargs["params"]
                    for key, value in params.items():
                        if key == 'taskGroupId':
                            params["taskGroupId"] = read_extract_yaml("taskGroupId")
                # elif key == "files":
                #     for file_key,file_path in value.items():
                #         value[file_key] = open(file_path,'rb')
        # 输出日志获取请求信息
        request_log(url, method, **kwargs)

        if method == "get" or method == "post" or method == "put" or method == "delete" or method == "patch":
            res = RequestUtil.session.request(method, self.url, **kwargs)
        else:
            logger.info('不支持的接口请求方式！')

        return res

    # 断言封装
    def validate_result(self, expect_result, actual_result, status_code):
        '''
        断言预期结果和实际结果是否正确
        expectResult: 期望结果
        actualResult: 实际结果
        status_code: 状态码
        '''

        # 定义一个断言成功与否的标记，0为成功，其他为失败
        flag_all = 0
        for expect in expect_result:
            for key, value in expect.items():
                print(key, value)
                if key == "equals":
                    flag = self.equals_assert(value, status_code, actual_result)
                    flag_all = flag_all + flag
                elif key == "contains":
                    flag = self.contains_assert(value, actual_result)
                    flag_all = flag_all + flag
                else:
                    logger.info("该断言还未添加，暂不支持")
        assert flag_all == 0

    # 相等断言
    def equals_assert(self, value, status_code, actual_result):
        flag = 0
        for assert_key, assert_value in value.items():
            # 判断断言状态是否一致
            if assert_key == "status_code":
                if assert_value != status_code:
                    flag = flag + 1
                    logger.info("断言失败，预期状态码{}返回的状态码{}".format(status_code, assert_value))
            else:
                assert_value_list = jsonpath.jsonpath(actual_result, f"$..{assert_key}")
                if assert_value_list:
                    if assert_value not in assert_value_list:
                        flag = flag + 1
                        logger.info(f"断言失败,{assert_key}不等于{assert_value}")
                else:
                    flag = flag + 1
                    logger.info(f"{assert_key}不存在")
        return flag

    # 包含断言
    def contains_assert(self, value, actual_result):
        flag = 0
        if value not in str(actual_result):
            flag = flag + 1
            logger.info(f"断言失败！{value}不存在{actual_result}中")
        return flag
