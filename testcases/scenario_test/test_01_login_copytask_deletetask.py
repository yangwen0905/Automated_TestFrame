import pytest
import allure
from service.common.yaml_operate_util import read_testcase_yaml
from service.api_interface.user_api import User
from service.api_interface.task_api import Task
from service.common.logger_util import logger


@allure.step("步骤1 ==>> 登录用户")
def step_1(username):
    logger.info("步骤1 ==>> 登录用户: {}".format(username))


@allure.step("步骤2 ==>> 复制task")
def step_2():
    logger.info("步骤2 ==>> 复制task")

@allure.step("步骤3 ==>> 删除task")
def step_3():
    logger.info("步骤3 ==>> 删除task: {}".format())


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：用户登录-复制任务-删除任务")
class TestLogCpDel():

    @allure.story("用例--用户登录-复制任务-删除任务")
    @allure.title("复制-删除-预期成功")
    @pytest.mark.multiple
    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("scenario_test/data/test_copy_delete.yaml"))
    def test_task_login_copy_delete(self, caseinfo):
        gettoken_data = caseinfo["login"]
        copytask_data = caseinfo["copytask"]
        deletetask_data = caseinfo["deletetask"]
        username = gettoken_data["request"]["data"]["username"]

        logger.info("*********************** 开始执行用例 ***********************")
        User.test_get_token(self, gettoken_data)
        step_1(username)
        Task.copytask(self, copytask_data)
        step_2()
        Task.deletetask(self, deletetask_data)
        step_3()
        logger.info("*********************** 结束执行用例 ***********************")


