# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import  json
import hashlib
import time
import platform
from abc import ABCMeta, abstractmethod
from loghandle import *
import platform


class db_baseline_basic(object):
    @staticmethod
    def getOption():
        return {}

    ##扫描基础类
    def __init__(self,runconfig):
        self.name = "DB_SECBaseLine"
        self.info = '''
[!] legal disclaimer: Usage of '''+self.name +''' for attacking targets withoutprior mutual consent is illegal.It is the end user's responsibilityto obey all applicable local,state and federal laws. Developersassume no liability and are notresponsible for any misuse or damagecaused by this program'''
        self.system = platform.system()
        self.path = platform.system()
        self.runconfig= runconfig #连接参数
        self.db = "" #数据库实例
        self.plog = loghandle.getLogEntity()
        self.result = {
            'DBInfo': {},  # 数据库信息
            'VerifyTime': {},  # 检查时间
            'Score': 100,  # 检查得分
            'Desc': "",  # 处理建议
            'Defect': []  # 缺陷列表
        }

    # 用于连接数据库
    @abstractmethod
    def connect(self):
        pass

    # 返回当前版本
    @staticmethod
    def getVersion():
        return "0.1"

    # 用于检查是否满足运行条件
    @abstractmethod
    def check(self):
        pass


    def getFilepower(self,path):
        try:
            pathdir =  os.path.dirname(os.path.abspath(path))
            basename = os.path.basename(os.path.abspath(path))
            command = 'ls -al ' + pathdir+"/   2>/dev/null | egrep '.*? "+basename+"$'  2>/dev/null | awk '{print $1}'"
            checkresult = os.popen(command).readlines()
            return   checkresult[0].strip("\n")
        except Exception,e:
            return  ""

    def runtest(self):
        print self.info
        self.result["VerifyTime"] = datetime.datetime.now().strftime('%H:%M:%S')
        self.result["endVerifyTime"] = ''

        print '''
[*]  starting at '''+self.result["VerifyTime"]+'''
'''
        self.plog.output("testing connection to the target")
        if self.connect():
            self.plog.output("Connect target success")
            checkenvir  =  self.check()
            self.plog.output("testing if the target envirment is suitable")

            if checkenvir:
                self.plog.output("target envirment is suitable")

            if platform.system() == "Windows":
                self.plog.output("Windows platfrom only run command teste", "WARNING")
            else:
                self.plog.output("testing power baseline")
                self.run_power_test()
                self.run_network_test()
                self.run_file_test()
            self.run_config_test()


        self.close()
        self.result["endVerifyTime"] = datetime.datetime.now().strftime('%H:%M:%S')

        for d1 in self.result['Defect']:
            if d1["Level"] == '低':
                self.result['Score'] = self.result['Score']-5
            elif  d1["Level"] == '中':
                self.result['Score'] = self.result['Score'] - 10
            else:
                self.result['Score'] = self.result['Score'] - 30

        if  self.result['Score']   == 100 :
            self.result['Desc'] = '系统状态优，无明显隐患'
        elif  self.result['Score']  > 70 :
            self.result['Desc'] ='系统状态良好，存在微小隐患'
        elif self.result['Score']  > 60 :
            self.result['Desc'] ='系统状态差，存在许多隐患'
        else:
            self.result['Desc'] = '系统状态十分危险，存在众多隐患'
        md5_C = hashlib.md5()
        md5_C.update(str(time.time()))

        print '''DB_Baseline check result :
---'''
        print 'Score:'+str(self.result['Score'])
        print 'Desc:'+str(self.result['Desc'])
        print 'Defect :'
        for r_item in self.result['Defect']:
            print  '    Defect:'+r_item['Desc']
            print  '    Level:'+r_item['Level']
            print  '    Suggest:'+r_item['Suggest']

        print '''---'''
        print '''
[*] test result save -> ./log/'''+ str(md5_C.hexdigest() ) +'''.log'''
        with open("./log/"+ str(md5_C.hexdigest() ) +".log","w") as f:
            f.writelines(json.dumps(self.result))


        print '''
[*] shutting down at '''+self.result["endVerifyTime"]+'''
        '''
        return self.result


    # 关闭连接
    @abstractmethod
    def close(self):
        pass

    # 账号权限基线检查
    @abstractmethod
    def run_power_test(self):
        pass

    # 网络连接基线检查
    @abstractmethod
    def run_network_test(self):
        pass

    # 文件安全基线检查
    @abstractmethod
    def run_file_test(self):
        pass

    # 数据库配置基线检查
    @abstractmethod
    def run_config_test(self):
        pass
