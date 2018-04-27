# DB_BASELINE 使用说明和检测脚本编写规范
![](https://github.com/wstart/DB_BaseLine/blob/master/image/1524419076653.jpg?raw=true)

![](https://github.com/wstart/DB_BaseLine/blob/master/image/3041524440631_.pic_hd.jpg?raw=true)

## 概述
本文档为DB_BASELINE的使用说明和检测脚本编写规范，
DB_BASELINE主要用于数据库的配置项的基线检查。
该文档主要描述了DB_BASELINE的使用方法以及检测脚本的编写规范，
编写规范检测脚本适用于后期导入SYSLOG，SOC等
## 支持的数据库
- mysql [基线检查详情=>mysql.md](https://github.com/wstart/DB_BaseLine/blob/master/doc/mysql.md)

## 安装说明
### 下载源码
- 直接下载 
- 或者 git clone https://github.com/wstart/DB_BaseLine 

### 安装依赖
- pip install -r requirements.txt

## DB_BASE 使用说明
- 帮助信息 python db_baseline.py -h
- 运行检查 python db_baseline.py [options]
- [*] 建议直接在运行数据库的机器上进行基线检查，如果不在运行数据库的机器上进行检查
  - 文件安全这一项无法进行
  - 部分数据库配置检查也无法进行

## DB_BASELINE 基线检查规范
根据查阅的资料和文档，虽然各个数据库有各自的配置，但是总的来说数据库的基线检查主要涵盖以下四类

- 账号权限
    - 检查运行数据库的账号，
    - 数据库里面各个权限账号
    - 检查方向：是否有过多的不必要的权限   
        - 用专有的低权限账号去启动数据库，而不是用root
        - 数据库账号不要空密码连接
        - 删除或者修改默认账号
        - 只有DBA拥有所有权限，其余各个数据库有专门的对应的数据库的账号
        - 数据库的账号要限制IP连接
        - ...
- 网络连接
    - 端口
    - 连接类型
    - 检查方向：主要用于检查数据库的端口，对外的开放的程度，连接的安全性等等 
        -  端口改掉默认端口
        - 如果提供对外访问 那么网络传输使用SSL或者其他加密的协议  
        - ...
  
- 文件安全
    - 配置文件
    - 日志文件
    - 审计文件
    - 备份文件
    - 检查方向：主要检查文件权限是否配置准确   
        - 配置文件，日志文件等应只有数据库账号可以访问
        - 限制数据库账号访问其他目录或者对其他目录有写的权限
        - ...
- 数据库配置的属性
    - 配置文件 
    - 可以执行的函数
    - 检查方向：潜在隐患的配置属性
        - 危险函数禁止执行
            - 执行系统命令
            - 读取文件
            - 写入文件
            - 导入导出
            - ... 
        - 安全配置是否开启
            - 日志文件是否开启
            - 审计文件是否开启
            - 错误日志是否开启
            - 密码复杂度
            - 过期账号处理
            - ... 
       
## DB_BASELINE 编写规范
所有的检测脚本均在script目录里面。

db_baseline_basic是检测类的基类,引用基类，编写对应的数据库的检查基线即可

## DB_BASELINE 基础构造
- 连接函数 connect 
- 用于检查是否满足运行条件 check
- 基线检查主函数 runtest 
    - 账号权限基线检查 run_power_test 
    - 网络连接基线检查 run_network_test 
    - 文件安全基线检查 run_file_test     
    - 数据库配置基线检查 run_config_test 
    
## DB_BASELINE 返回值
```
'Result':{
   'DBInfo' :   {'Host': 'xxx', 'Port': 'xxx'}, #数据库信息
   'VerifyTime': '2018-03-23' ,#检查时间
   'Score': 97,#检查得分
   'Desc': '几乎没有严重的问题',#处理建议
   'Defect':
    [
        {
            'Desc':'默认端口没有修改',#描述
            'Level':'低',# 危害等级 
            'Suggest':'修改默认端口',# 修复建议
        }
    ]
}
```

## TODO
- mongo 基线检查
- oracle  基线检查
- redis 基线检查
- sqlserver 基线检查

## 更新记录
- 2017-04-27
    - 重新修改检测的类别，以及对应修改了代码，比以前类别更加清晰
    - 增加了mysql的检查项的类别 
- 2017-04-24  
    - 0.1 发布，基础架构和雏形
    - mysql 基线检查 

