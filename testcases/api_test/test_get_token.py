import requests
import pytest
from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import clean_loginToken_yaml, write_loginToken_yaml, read_testcase_yaml





class TestGettoken():

    @pytest.mark.parametrize("tokeninfo",read_testcase_yaml("api_test/test_get_token.yaml"))
    def test_get_token(self, tokeninfo):
        method = tokeninfo["request"]["method"]
        url = tokeninfo["request"]["url"]
        headers = tokeninfo["request"]["headers"]
        datas = tokeninfo["request"]["datas"]
        
        res = RequestUtil().send_token_request(method=method,url=url,headers=headers,data=datas)
        
        assert res.status_code == tokeninfo["vilidate"]["codes"]

        
        #判断是否成功登录，若成功，则把token值存入extract.yaml
        #token时效性20分钟
        if "access_token" in dict(res.json()).keys():
            clean_loginToken_yaml()
            write_loginToken_yaml({"Authorization": res.json()["access_token"]})

