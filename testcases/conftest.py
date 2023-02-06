# import pytest
# import os
# import allure
# from service.common.requests_util import
# # from service.common.mysql_operate import db
# from service.common.read_data_util import data
# from service.common.logger_util import logger

# BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# def get_data(yaml_file_name):
#     try:
#         data_file_path = os.path.join(BASE_PATH, "data", yaml_file_name)
#         yaml_data = data.load_yaml(data_file_path)
#     except Exception as ex:
#         pytest.skip(str(ex))
#     else:
#         return yaml_data


# base_data = get_data("base_data.yml")
# api_data = get_data("api_test_data.yml")
# scenario_data = get_data("scenario_test_data.yml")


# @allure.step("ǰ�ò��� ==>> ����Ա�û���¼")
# def step_login(username, password):
#     logger.info("ǰ�ò��� ==>> ����Ա {} ��¼��������Ϣ Ϊ��{}".format(username, password))


# @pytest.fixture(scope="session")
# def login_fixture():
#     username = base_data["init_admin_user"]["username"]
#     password = base_data["init_admin_user"]["password"]
#     header = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     payload = {
#         "username": username,
#         "password": password
#     }
#     loginInfo = RequestType().post(data=payload, headers=header)
#     step_login(username, password)
#     yield loginInfo.json()