import requests
import pytest

from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import read_loginToken_yaml, write_loginToken_yaml, read_testcase_yaml


class TestTaskInfo():

    # 获取TaskGroup信息
    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("api_test/test_get_taskgrouplist.yaml"))
    def test_get_taskgrouplist(self, caseinfo):
        res = RequestUtil().standard_yaml(caseinfo)

    # 获取获取TaskGroup信息中Task信息
    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("api_test/test_get_tasklist.yaml"))
    def test_get_tasklist(self, caseinfo):

        # params = caseinfo["request"]["params"]
        # params["taskGroupId"] = str(TestTaskInfo.taskgroupid)
        res = RequestUtil().standard_yaml(caseinfo)
