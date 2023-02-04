import allure
import requests
import pytest

from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import read_loginToken_yaml, write_loginToken_yaml, read_testcase_yaml


@allure.epic("针对单个接口的测试")
@allure.feature("任务列表模块")
class TestTaskInfo():

    # 获取TaskGroup信息
    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("api_test/test_get_taskgrouplist.yaml"))
    def test_get_taskgrouplist(self, caseinfo):
        res = RequestUtil().standard_yaml(caseinfo)
        allure.dynamic.story(caseinfo["story"])
        allure.dynamic.title(caseinfo["title"])

    # 获取获取TaskGroup信息中Task信息
    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("api_test/test_get_tasklist.yaml"))
    def test_get_tasklist(self, caseinfo):
        # params = caseinfo["request"]["params"]
        # params["taskGroupId"] = str(TestTaskInfo.taskgroupid)
        res = RequestUtil().standard_yaml(caseinfo)
        allure.dynamic.story(caseinfo["story"])
        allure.dynamic.title(caseinfo["title"])
