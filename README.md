# DB_BASELINE 使用说明和检测脚本编写规范
![](https://github.com/wstart/DB_BaseLine/blob/master/image/1524419076653.jpg?raw=true)

![](https://github.com/wstart/DB_BaseLine/blob/master/image/3041524440631_.pic_hd.jpg?raw=true)

## 概述
本文档为DB_BASELINE的使用说明和检测脚本编写规范，
DB_BASELINE主要用于数据库的配置项的基线检查。
该文档主要描述了DB_BASELINE的使用方法以及检测脚本的编写规范，
编写规范检测脚本适用于后期导入SYSLOG，SOC等
## DB_BASE 使用说明
- 帮助信息 python db_baseline.py -h

## DB_BASELINE 检查规范
根据查阅的资料和文档，基线检查主要分为以下四类

- 账号权限
检查各个权限账号是否有过多的不必要的权限，检查数据库的文件的权限，是否只归属数据库账户所有，其他程序是否可读可写，
 
- 网络连接
主要用于检查数据库的端口，对外的开放的程度，连接的安全性等等

- 危险语句
主要检查数据库是否可以运行危险语句

- 配置文件
主要检查数据库的配置文件是否规范合理 

## DB_BASELINE 编写规范
所有的检测脚本均在script目录里面。

db_baseline_basic是检测类的基类,引用基类，编写对应的数据库的检查基线即可

## DB_BASELINE 基础构造
- 连接函数 connect 
- 用于检查是否满足运行条件 check
- 基线检查主函数 runtest 
    - 账号权限基线检查 run_power_test 
    - 网络连接基线检查 run_netword_test 
    - 危险语句基线检查 run_exec_test     
    - 配置文件基线检查 run_config_test 
    
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

#TODO
- mongo 基线检查
- oracle  基线检查
- redis 基线检查
- sqlserver 基线检查

#更新记录
- 2017-04-24  
    - 0.1 发布，基础架构和雏形
    - mysql 基线检查 

