import pytest
from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import clean_loginToken_yaml, write_loginToken_yaml, read_testcase_yaml


class TestGettoken():

    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("api_test/test_get_token.yaml"))
    def test_get_token(self, caseinfo):
        # method = tokeninfo["request"]["method"]

        # assert res.status_code == tokeninfo["vilidate"]["codes"]
        res = RequestUtil().standard_yaml(caseinfo)
