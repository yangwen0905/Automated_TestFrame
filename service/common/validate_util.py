
import jsonpath
from service.common.logger_util import LoggerUtil, logger


class Validate():
# 断言封装
    def validate_result(self, expect_result, actual_result, status_code):
        '''
        断言预期结果和实际结果是否正确
        expectResult: 期望结果
        actualResult: 实际结果
        status_code: 状态码
        '''

        # 定义一个断言成功与否的标记，0为成功，其他为失败
        flag_all = 0
        for expect in expect_result:
            for key, value in expect.items():
                logger.info("断言方式：{},预期结果：{}".format(key,value))
                if key == "equals":
                    flag = Validate.equals_assert(value, status_code, actual_result)
                    flag_all = flag_all + flag
                elif key == "contains":
                    flag = Validate.contains_assert(value, actual_result)
                    flag_all = flag_all + flag
                else:
                    logger.info("该断言还未添加，暂不支持")
            assert flag_all == 0
        


    # 相等断言
    def equals_assert(value, status_code, actual_result):
        flag = 0
        for assert_key, assert_value in value.items():
            # 判断断言状态是否一致
            if assert_key == "status_code":
                if assert_value != status_code:
                    flag = flag + 1
                    logger.info("断言失败，预期状态码{}返回的状态码{}".format(assert_value, status_code))
            else:
                assert_value_list = jsonpath.jsonpath(actual_result, f"$..{assert_key}")
                if assert_value_list:
                    if assert_value not in assert_value_list:
                        flag = flag + 1
                        logger.info(f"断言失败,{assert_key}不等于{assert_value}")
                else:
                    flag = flag + 1
                    logger.info(f"{assert_key}不存在")
        return flag

    # 包含断言
    def contains_assert(value, actual_result):
        flag = 0
        if value not in str(actual_result):
            flag = flag + 1
            logger.info(f"断言失败！{value}不存在{actual_result}中")
        return flag
    
validate = Validate()