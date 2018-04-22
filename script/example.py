# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import db_baseline_basic


class example_baseline(db_baseline_basic):
    def connect(self): pass

    # 用于检查是否满足运行条件

    def check(self): pass

    # 开始基线检查

    def runtest(self): pass

    # 文件权限基线检查

    def run_file_test(self): pass

    # 网络基线检查

    def run_net_test(self): pass

    # 权限基线检查

    def run_power_test(self): pass

    # 配置基线检查

    def run_setting_test(self): pass


# 数据文件位置检查
#sql = "show variables where variable_name = 'datadir';"
#result = self.getOneLine(sql)
#checkresult = os.popen('df -h ' + result[1]).readlines()
#if "/dev/disk1s1" in checkresult[1]:
#    self.result["Defect"].append(
#       {
#           'Desc': '文件存放在系统目录容易损坏',  # 描述
#            'Level': '低',  # 危害等级
#            'Suggest': '修改配置文件中datadir的值',  # 修复建议
#        }
#    )
