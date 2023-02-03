import requests
import pytest
from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import read_loginToken_yaml,write_loginToken_yaml, read_testcase_yaml






class TestTaskInfo():

    taskgroupid = ""

    #获取TaskGroup信息
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml("api_test/test_get_taskgrouplist.yaml"))
    def test_get_taskgrouplist(self, caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        #传参token
        headers = caseinfo["request"]["headers"]
        headers["Authorization"] = "Bearer "+read_loginToken_yaml("Authorization")
        res = RequestUtil().send_request(method=method,url=url,headers=headers)
        

        if '我的任务组' in res.json()['data'][0].values():
            TestTaskInfo.taskgroupid = res.json()["data"][0]["taskGroupId"]
            print("TestTaskInfo.taskgroupid: "+str(TestTaskInfo.taskgroupid))

        

    #获取获取TaskGroup信息中Task信息
    @pytest.mark.parametrize("caseinfo",read_testcase_yaml("api_test/test_get_tasklist.yaml"))
    def test_get_tasklist(self, caseinfo):
        method = caseinfo["request"]["method"]
        url = caseinfo["request"]["url"]
        #传参token
        headers = caseinfo["request"]["headers"]
        headers["Authorization"] = "Bearer "+read_loginToken_yaml("Authorization")

        params = caseinfo["request"]["params"]
        params["taskGroupId"] = str(TestTaskInfo.taskgroupid)
        res = RequestUtil().send_request(method=method,url=url,headers=headers,params=params)
        

