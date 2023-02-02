<<<<<<< HEAD
# pytestDemo

实现接口自动化的技术选型：**Python+Requests+Pytest+YAML+Allure** ，主要是针对本人的一个接口项目来开展的，通过 Python+Requests 来发送和处理 HTTP 协议的请求接口，使用 Pytest 作为测试执行器，使用 YAML 来管理测试数据，使用 Allure 来生成测试报告。

## 项目说明

本项目在实现过程中，把整个项目拆分成请求方法封装、HTTP 接口封装、关键字封装、测试用例等模块。

首先利用 Python 把 HTTP 接口封装成 Python 接口，接着把这些 Python 接口组装成关键字，再把关键字组装成测试用例，而测试数据则通过 YAML 文件进行统一管理，然后再通过 Pytest 测试执行器来运行这些脚本，并结合 Allure 输出测试报告。

当然，如果感兴趣的话，还可以再对接口自动化进行 Jenkins 持续集成。

## 项目部署

首先，下载项目源码后，在根目录下找到 `requirements.txt` 文件，然后通过 pip 工具安装 requirements.txt 依赖，执行命令：

```
pip3 install -r requirements.txt
```

接着，修改 `config/setting.ini` 配置文件，在 Windows 环境下，安装相应依赖之后，在命令行窗口执行命令：

```
pytest
```

## 项目结构

- common ====>> 公共封装文件：如：日志模块，读取分析各文件类型模块
- api ====>> 接口封装层，如封装 HTTP 接口为 Python 接口
- core ====>> requests 请求方法封装、关键字返回结果类
- config ====>> 配置文件
- data ====>> 测试数据文件管理
- operation ====>> 关键字封装层，如把多个 Python 接口封装为关键字
- pytest.ini ====>> pytest 配置文件
- requirements.txt ====>> 相关依赖包文件
- testcases ====>> 测试用例


## yaml编写测试用例常规格式及可用关键字

  feature: 模块名（必填）
  story: 接口名（必填）
  title: 用例标题（必填）
  request: 请求
    method: 请求方式（必填）
    url: 请求地址（必填）
    headers: 请求头
    params: (显性参数)
    data: {请求表单)
    json: 
    file: (文件上传)
  vilidate: 断言（必填）
    codes
    equals
    contains
    db_equals

## 测试报告效果展示

在命令行执行命令：`pytest` 运行用例后，执行命令启动 `allure` 服务：
allure serve ./report

```
# 需要提前配置allure环境

  官网下载安装包，配置变量环境path

  注：配置好变量环境后需重启编辑器
```

