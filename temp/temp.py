res = {'data': [
            {'taskGroupId': 3279398, 'taskGroupName': '我的任务组'}, {
    'taskGroupId': 3288969, 'taskGroupName': '图片bug'}], 'error': 'success'}

taskgroupid = ""
taskgroupid = res['data']
test = ""

if '我的任务组' in taskgroupid[0].values():
    test = res["data"][0]["taskGroupId"]

    
if __name__ == '__main__':
    print(test.type())
