import allure
import requests
import pytest

from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import read_testcase_data_yaml


@allure.epic("针对单个接口的测试")
@allure.feature("用户信息模块")
class TestUserInfo():

    # 获取TaskGroup信息
    @pytest.mark.parametrize("caseinfo", read_testcase_data_yaml("single_test_data/test_user_basic.yaml"))
    def test_get_taskgrouplist(self, caseinfo):
        res = RequestUtil().send_request(caseinfo)
        allure.dynamic.story(caseinfo["story"])
        allure.dynamic.title(caseinfo["title"])