import requests
import pytest
from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import read_loginToken_yaml,write_loginToken_yaml, read_testcase_yaml





class TestTaskInfo():

    taskgroupid = ""

    #获取TaskGroup信息
    @pytest.mark.parametrize("taskgrouplistinfo",read_testcase_yaml("api_test/test_get_taskgrouplist.yaml"))
    def test_get_taskgrouplist(self, taskgrouplistinfo):
        method = taskgrouplistinfo["request"]["method"]
        url = taskgrouplistinfo["request"]["url"]
        #传参token
        headers = taskgrouplistinfo["request"]["headers"]
        headers["Authorization"] = "Bearer "+read_loginToken_yaml("Authorization")
        
        res = RequestUtil().send_request(method=method,url=url,headers=headers)
        print(res.json())

        if '我的任务组' in res.json()['data'][0].values():
            TestTaskInfo.taskgroupid = res.json()["data"][0]["taskGroupId"]
            print(TestTaskInfo.taskgroupid)

        

    #获取获取TaskGroup信息中Task信息
    @pytest.mark.parametrize("tasklistinfo",read_testcase_yaml("api_test/test_get_tasklist.yaml"))
    def test_get_tasklist(self, tasklistinfo):
        method = tasklistinfo["request"]["method"]
        url = tasklistinfo["request"]["url"]
        #传参token
        headers = tasklistinfo["request"]["headers"]
        headers["Authorization"] = "Bearer "+read_loginToken_yaml("Authorization")

        params = tasklistinfo["request"]["params"]
        params["taskGroupId"] = TestTaskInfo.taskgroupid
        res = RequestUtil().send_request(method=method,url=url,headers=headers,params=params)
        print(res.json())

