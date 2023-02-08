from service.common.validate_util import Validate, validate
from service.common.requests_util import RequestUtil
from service.common.yaml_operate_util import write_extract_yaml, read_extract_yaml


class Task():
    '''获取任务组列表'''
    def get_taskgrouplist(self, caseinfo):
        res = RequestUtil().send_request(caseinfo)
        return_text = res.text
        return_code = res.status_code
        return_json = res.json()

        validate.validate_result(caseinfo["validate"], return_json, return_code)

        # 判断是否有数据，若有，则把“我的任务组”的id存入extract.yaml
        if "data" in dict(return_json).keys():
            return_json_data = return_json["data"]
            for item_dict in return_json_data:
                if "taskGroupName" in item_dict and item_dict["taskGroupName"] == "我的任务组":
                    write_extract_yaml({"taskGroupId": item_dict["taskGroupId"]})
        
    '''获取某任务组中任务列表'''
    def get_tasklist(self, caseinfo):
        res = RequestUtil().send_request(caseinfo)
        return_text = res.text
        return_code = res.status_code
        return_json = res.json()

        validate.validate_result(caseinfo["validate"], return_json, return_code)
    
    '''复制任务列表'''
    def copytask(self, caseinfo):
        res = RequestUtil().send_request(caseinfo)
        return_text = res.text
        return_code = res.status_code
        return_json = res.json()

        validate.validate_result(caseinfo["validate"], return_json, return_code)

        if "data" in dict(return_json).keys():
            write_extract_yaml({"taskId": return_json["data"]})

    '''删除任务列表'''
    def deletetask(self, caseinfo):
        res = RequestUtil().send_request(caseinfo)
        return_text = res.text
        return_code = res.status_code
        return_json = res.json()

        validate.validate_result(caseinfo["validate"], return_json, return_code)