
import json as complexjson
from service.common.logger_util import LoggerUtil, logger
from service.common.yaml_operate_util import read_config_yaml, read_extract_yaml, read_loginToken_yaml, read_extract_yaml_list

'''解析yaml测试用例'''
class YamlAnalysis():

    def standard_yaml(self, caseinfo):
        caseinfo_keys = caseinfo.keys()
        last_caseinfo = caseinfo
        # 判断以及关键字是否包含：story，request,validate
        if "story" in caseinfo_keys and "title" in caseinfo_keys \
                and "request" in caseinfo_keys and "validate" in caseinfo_keys:
            request_keys = caseinfo["request"].keys()

            # 判断request下面是否包含：method、url
            if "method" in request_keys and "url" in request_keys:
                logger.info("yaml基本架构检查通过")
                
                #method参数转换为小写
                self.method = str(caseinfo["request"].pop("method")).lower()
                last_caseinfo["method"] = self.method
                url = caseinfo["request"].pop("url")
                
                if url == "token":
                    self.url = self.auth_base_url + url
                    last_caseinfo["url"] = self.url
                else:
                    self.url = self.base_url + url
                    last_caseinfo["url"] = self.url

                    headers = caseinfo["request"]["headers"]
                    headers["Authorization"] = "Bearer " + read_loginToken_yaml("Authorization")
                    last_caseinfo["headers"] = headers
                # 参数替换
                kwargs = caseinfo['request']

                # 针对某些前置参数值的获取
                for key, value in kwargs.items():
                    if key == 'params':
                        params = kwargs["params"]
                        for key, value in params.items():
                            if key == 'taskGroupId':
                                params["taskGroupId"] = read_extract_yaml("taskGroupId")
                                last_caseinfo["params"] = params
                    if key == 'json':
                        json = kwargs["json"]
                        for key, value in json.items():
                            if key == 'taskIds':
                                json["taskIds"] = read_extract_yaml_list("taskIds")
                                last_caseinfo["json"] = json
                    # elif key == "files":
                    #     for file_key,file_path in value.items():
                    #         value[file_key] = open(file_path,'rb')   
                try:
                    return last_caseinfo
                except Exception as e:
                    logger.info("extract返回的结果不是JSON格式")
            else:
                logger.info("request中必须包含method, url")
        else:
            logger.info("一级关键字必须包含story, title")
            
    '''yaml参数替换'''
    def replace_value(self, data):
        if data:
            # 保存数据类型
            data_type = type(data)
            # 判断数据类型转换成str
            if isinstance(data, dict) or isinstance(data, list):
                str_data = complexjson.dumps(data)
            else:
                str_data = str(data)
            for cs in range(1, str_data.count('${') + 1):
                if "${" in str_data and "} " in str_data:
                    start_index = str_data.index('${')
                    end_index = str_data.index('}', start_index)
                    old_value = str_data[start_index:end_index + 1]
                    print("old_value:" + old_value)
                    # 反射：通过类的对象和方法字符串调用方法
                    func_name = old_value[2:old_value.index('(')]
                    args_value1 = old_value[old_value.index('(') + 1:old_value.index(')')]
                    new_value = ""
                    if args_value1 != "":
                        args_value2 = args_value1.split(',')
                        new_value = getattr(self.obj, func_name)(*args_value2)
                    else:
                        new_value = getattr(self.obj, func_name)()
                    str_data = str_data.replace(old_value, str(new_value))
            # 还原数据类型
            if isinstance(data, dict) or isinstance(data, list):
                data = complexjson.loads(str_data)
            else:
                data = data_type(str_data)
            return data