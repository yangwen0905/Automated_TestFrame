import os
import time
import pytest
import allure
from service.common.yaml_operate_util import read_testcase_yaml


if __name__ == '__main__':
    pytest.main()
    time.sleep(5)
    os.system("allure serve ./report")
