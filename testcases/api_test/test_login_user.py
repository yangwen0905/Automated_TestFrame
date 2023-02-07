import allure
import pytest
from service.api_interface.user_api import User
from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import clean_loginToken_yaml, write_loginToken_yaml, read_testcase_yaml


@allure.epic("针对单个接口的测试")
@allure.feature("用户登录模块")
class TestGettoken():

    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("api_test/data/test_get_token.yaml"))

    def test_get_token(self, caseinfo):
        User().test_get_token(caseinfo)
        allure.dynamic.story(caseinfo["story"])
        allure.dynamic.title(caseinfo["title"])
