import jsonpath
import requests
import re
import json as complexjson
from service.common.yaml_analysis_util import YamlAnalysis
from service.common.yaml_operate_util import read_loginToken_yaml, read_config_yaml, clean_loginToken_yaml, \
    write_loginToken_yaml, read_extract_yaml, write_extract_yaml
from service.common.logger_util import LoggerUtil, logger





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

        return_text = res.text
        return_code = res.status_code
        return_json = res.json()

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
        
        self.validate_result(last_caseinfo["validate"], return_json, return_code)
        

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
                logger.info("断言方式：{},预期结果：{}".format(key,value))
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
