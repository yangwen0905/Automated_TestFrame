
from service.common.validate_util import Validate, validate
from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import clean_loginToken_yaml, write_loginToken_yaml


class User():
    #封装接口为关键字，供单接口用例和场景用例共同调用
    def test_get_token(self, caseinfo):
        res = RequestUtil().send_request(caseinfo)
        return_text = res.text
        return_code = res.status_code
        return_json = res.json()

        validate.validate_result(caseinfo["validate"], return_json, return_code)

        # 判断是否成功登录，若成功，则把token值存入loginToken.yaml
        # token时效性20分钟
        if "access_token" in dict(return_json).keys():
            clean_loginToken_yaml()
            write_loginToken_yaml({"Authorization": return_json["access_token"]})
    
    def user_basic(self, caseinfo):
        res = RequestUtil().send_request(caseinfo)
        return_text = res.text
        return_code = res.status_code
        return_json = res.json()

        validate.validate_result(caseinfo["validate"], return_json, return_code)

        
        