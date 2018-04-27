# -*- coding: utf-8 -*-
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

from db_baseline_basic import *
import pymysql


class mysql_baseline(db_baseline_basic):
    def connect(self):

        # print  self.runconfig
        host = self.runconfig["host"]
        database_port = self.runconfig["database_port"]
        database_user = self.runconfig["database_user"]
        database_password = self.runconfig["database_password"]
        if host == "":
            host = '127.0.0.1'
        if database_port == "" or database_port == 0:
            database_port = 3306

        else:
            database_port = int(database_port)
        if database_user == "":
            database_user = "root"
        if database_password == "":
            database_password = ""
        try:
            self.db = pymysql.connect(host=host, user=database_user, passwd=database_password, port=database_port)
            self.cursor = self.db.cursor()
            return True
        except Exception, e:
            self.plog.output(e, "CRITICAL")
            return False

    def check(self):
        return True

    # 账号权限基线检查
    def run_power_test(self):
        # 启动 mysql 的系统账号 是否单独创建 且 不允许登陆
        checkresult = os.popen(' cat /etc/passwd  | grep  mysql ').readlines()
        if len(checkresult) != 0:
            checkresult = os.popen(' cat /etc/passwd  | grep  mysql | grep /usr/bin/false').readlines()
            if len(checkresult) == 0:
                checkresult = os.popen(' cat /etc/passwd  | grep  mysql | grep /usr/sbin/nologin').readlines()
            if len(checkresult) == 0:
                self.plog.output("run mysql  system account can login  ", "ERROR")
                self.result["Defect"].append(
                    {
                        'Desc': '运行mysql的用户可以登陆',  # 描述
                        'Level': '中',  # 危害等级
                        'Suggest': '禁止运行mysql的用户登陆，添加/usr/bin/false 或  /usr/sbin/nologin',  # 修复建议
                    }
                )
        else:
            self.plog.output("Run mysql account not found ", "WARNING")
            self.result["Defect"].append(
                {
                    'Desc': '没有找到运行mysql程序的系统用户',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '单独为mysql执行添加系统用户',  # 修复建议
                }
            )
        self.plog.output("run mysql  account check finish ")

        #检查默认管理员账号
        sql = "SELECT * from MySQL.user where user='root';"
        result = self.getOneLine(sql)
        if len(result) > 0:
            self.plog.output("default user root exits", "ERROR")
            self.result["Defect"].append(
                {
                    'Desc': '默认管理员账号存在',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '修改名字或者删除',  # 修复建议
                }
            )
        self.plog.output("default user root check finish")


        #高级权限账号 是否 为管理员账号
        sql="SELECT user, host FROM mysql.user WHERE (Select_priv = 'Y') OR (Insert_priv = 'Y') OR (Update_priv = 'Y') OR (Delete_priv = 'Y') OR (Create_priv = 'Y') OR (Drop_priv = 'Y');  "
        result = self.getAllLine(sql)
        if  len(result) > 0:
            self.plog.output("Please make sure this high level account is root:","ERROR")
            root_account = []
            for r_item in result:
                root_account_string = r_item[0]+","+r_item[1]
                self.plog.output( root_account_string,"ERROR",showlevel=False,showtime=False)
                root_account.append(root_account_string)
            self.result["Defect"].append(
                {
                    'Desc': '确保以下的账号都是管理员账号'+ "\n".join( root_account),  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '删除非管理员账号',  # 修复建议
                }
            )



        #系统数据库的高级权限账号是否必须
        sql = "SELECT user, host FROM mysql.db WHERE db = 'MySQL' AND ((Select_priv = 'Y') OR (Insert_priv = 'Y') OR (Update_priv = 'Y') OR (Delete_priv = 'Y') OR (Create_priv = 'Y') OR (Drop_priv = 'Y'));"
        result = self.getAllLine(sql)
        if  len(result) > 0:
            self.plog.output("Please make sure this   high level  account is root:","ERROR")
            root_account = []
            for r_item in result:
                root_account_string = r_item[0]+","+r_item[1]
                self.plog.output( root_account_string,"ERROR",showlevel=False,showtime=False)
                root_account.append(root_account_string)
            self.result["Defect"].append(
                {
                    'Desc': '确保以下的账号都是管理员账号'+ "\n".join( root_account),  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '删除非管理员账号',  # 修复建议
                }
            )
        self.plog.output("test high level user finish")

        #具有某个高级权限账号 是否必须
        high_level_priv = []
        high_level_priv.append({"name": "File_priv", "desc": "文件权限"})
        high_level_priv.append({"name": "Process_priv", "desc": "进程权限"})
        high_level_priv.append({"name": "Super_priv", "desc": "委托权限"})
        high_level_priv.append({"name": "Shutdown_priv", "desc": "关闭权限"})
        high_level_priv.append({"name": "Create_user_priv", "desc": "创建用户权限"})
        high_level_priv.append({"name": "Grant_priv", "desc": "赋权权限"})
        high_level_priv.append({"name": "reload_priv", "desc": "重载权限"})
        high_level_priv.append({"name": "repl_slave_priv", "desc": "主从数据库权限"})

        for h_item in high_level_priv:
            sql = "select user, host from mysql.user where " + h_item["name"] + " = 'Y' "
            result = self.getAllLine(sql)
            if len(result) > 0:
                self.plog.output("Please make sure this high level " + h_item["name"] + " account is root:", "ERROR")
                root_account = []
                for r_item in result:
                    root_account_string = r_item[0] + "," + r_item[1]
                    self.plog.output(root_account_string, "ERROR", showlevel=False, showtime=False)
                    root_account.append(root_account_string)
                self.result["Defect"].append(
                    {
                        'Desc': '以下的账号拥有' + h_item["desc"] + '，请确保是管理员账号' + "\n".join(root_account),  # 描述
                        'Level': '低',  # 危害等级
                        'Suggest': '删除非管理员账号',  # 修复建议
                    }
                )
            self.plog.output("test high level  " + h_item["name"] + " user finish")

        #密码为空的账号是否存在
        sql ="select * from INFORMATION_SCHEMA.COLUMNS  where TABLE_SCHEMA = 'mysql' and TABLE_NAME='user' and COLUMN_NAME='authentication_string' limit 1;"
        result = self.getOneLine(sql)
        if result > 0:
            sql = "SELECT User,host FROM mysql.user WHERE authentication_string='';"
        else :
            sql = "SELECT User,host FROM mysql.user WHERE password='';      ;"

        result = self.getAllLine(sql)
        if len(result) > 0:
            self.plog.output(" Null password user exits ", "ERROR")
            root_account = []
            for r_item in result:
                root_account_string = r_item[0] + "," + r_item[1]
                self.plog.output(root_account_string, "ERROR", showlevel=False, showtime=False)
                root_account.append(root_account_string)

            self.result["Defect"].append(
                {
                    'Desc': '存在空账号' + "\n".join(root_account),  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '为空密码账号添加密码',  # 修复建议
                }
            )
        self.plog.output("test Null password user finish")


        #不受IP限制的账号
        sql = "SELECT user, host FROM mysql.user WHERE host = '%';"
        result = self.getAllLine(sql)
        if len(result) > 0:
            self.plog.output("all ip access account exits ", "ERROR")
            root_account = []
            for r_item in result:
                root_account_string = r_item[0] + "," + r_item[1]
                self.plog.output(root_account_string, "ERROR", showlevel=False, showtime=False)
                root_account.append(root_account_string)

            self.result["Defect"].append(
                {
                    'Desc': '存在允许所有IP访问的账号' + "\n".join(root_account),  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '限制IP访问去掉%',  # 修复建议
                }
            )
        self.plog.output("test all ip access account finish")

        #空用户账号
        sql  ="SELECT user,host FROM mysql.user WHERE user = '';"
        result = self.getAllLine(sql)
        if len(result) > 0:
            self.plog.output("null name account exits ", "ERROR")
            root_account = []
            for r_item in result:
                root_account_string = r_item[0] + "," + r_item[1]
                self.plog.output(root_account_string, "ERROR", showlevel=False, showtime=False)
                root_account.append(root_account_string)

            self.result["Defect"].append(
                {
                    'Desc': '存在空用户名的账号号' + "\n".join(root_account),  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '删除空用户名账号',  # 修复建议
                }
            )
        self.plog.output("test null name  account finish")


    # 网络连接基线检查
    def run_network_test(self):
        sql = "show global variables like 'port';"
        result = self.getOneLine(sql)

        if len(result) > 0 and result[1] == '3306':
            self.plog.output("default port  now is " + result[1]+" not safe ","ERROR")
            self.result["Defect"].append(
                {
                    'Desc': ' 默认端口没有修改',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '修改肥3306端口',  # 修复建议
                }
            )
        self.plog.output("test default port check finish")


        sql = "SHOW variables WHERE variable_name = 'have_ssl';"
        result = self.getOneLine(sql)
        if len(result)  > 0  and   result[1] != 'yes' :
            self.plog.output("SSL is not set , now is " + result[1]+" not safe ","ERROR")
            self.result["Defect"].append(
                {
                    'Desc': ' 网络请求未走 SSL 连接',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '开启 ssh',  # 修复建议
                }
            )
        self.plog.output("test SSL CONNECT  check finish")
        pass

    # 文件安全基线检查
    def run_file_test(self):
        # 数据文件位置检查
        sql = "show variables where variable_name = 'datadir';"
        result = self.getOneLine(sql)
        checkresult = os.popen('df -h ' + result[1]).readlines()
        if "/var/usr" in checkresult[1]:
            self.plog.output("DataBase file path not safe", "ERROR")
            self.result["Defect"].append(
                {
                    'Desc': '数据文件存放在系统目录容易损坏',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '修改配置文件中datadir的值',  # 修复建议
                }
            )
        self.plog.output("DataBase file path check finish")

        checkresult = self.getFilepower(result[1])
        if checkresult != "":
            if "drwx------" != checkresult:
                self.plog.output("DataBase file Permissions error ,should be 700，now is " + checkresult+"", "ERROR")
                self.result["Defect"].append(
                    {
                        'Desc': '文件存放在系统目录容易损坏',  # 描述
                        'Level': '低',  # 危害等级
                        'Suggest': '修改配置文件中datadir的值',  # 修复建议
                    }
                )
        else:
            self.plog.output("Access  " + result[1] + " fail，please confirm Permissions is 700", "WARNING")
        self.plog.output("DataBase file Permissions check finish")


        # 检查MYSQL命令执行历史记录
        checkresult = os.popen('find ~/.mysql_history  2>/dev/null').readlines()
        if len(checkresult) > 0:
            self.plog.output(".mysql_history exits ", "ERROR")
            self.result["Defect"].append(
                {
                    'Desc': '存在MYSQL命令执行历史记录',  # 描述
                    'Level': '中',  # 危害等级
                    'Suggest': '存在.mysql_history文件且禁止生成',  # 修复建议
                }
            )

        # 敏感日志文件权限检查
        dangerfile_list = []
        dangerfile_list.append({"name": "log_bin_basename", "desc": "日志二进制文件 用于恢复和备份数据库"})
        dangerfile_list.append({"name": "log_error", "desc": "错误日志文件"})
        dangerfile_list.append({"name": "slow_query_log_file", "desc": "慢查询文件"})
        dangerfile_list.append({"name": "general_log_file", "desc": "通用日志文件"})
        dangerfile_list.append({"name": "audit_log_file", "desc": "审计日志文件"})
        dangerfile_list.append({"name": "relay_log_basename", "desc": "中转日志文件的名称和路径"})

        for file_item in dangerfile_list:
            sql = "show variables where variable_name = '" + file_item["name"] + "';"
            result = self.getOneLine(sql)
            #print result
            if result == None or len(result) == 0 or result[1] == "":
                self.plog.output(file_item["name"] + " is empty and can not locat   ", "ERROR")
            else:
                filepath = result[1]
                file_right = self.getFilepower(filepath)
                if file_right == "":
                    self.plog.output("Access "+file_item['name'] +'->'+ filepath + " fail，please confirm Permissions is 600",
                                     "WARNING")
                else:
                    if file_right != "-rwx------":
                        self.plog.output("DATABASE FILE   " + filepath + " should be 700，now is " + result[1], "ERROR")
                        self.result["Defect"].append(
                            {
                                'Desc': file_item["name"] + '文件权限有误',  # 描述
                                'Level': '低',  # 危害等级
                                'Suggest': '修改' + file_item["name"] + '文件权限的值为600',  # 修复建议
                            }
                        )
            self.plog.output(file_item["name"] + " check finish")
        pass


    # 数据库配置基线检查
    def run_config_test(self):
        sql = "SHOW variables LIKE 'log_error';"
        result = self.getOneLine(sql)
        if len(result ) <=0 or result[1]  == '':
            self.plog.output("Error log is close ", "ERROR")
            self.result["Defect"].append(
                {
                    'Desc': '错误日志没有打',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '配置错误日志',  # 修复建议
                }
            )
        self.plog.output("test error log finish")


        sql ="SHOW GLOBAL VARIABLES LIKE 'log_warnings';"
        result = self.getOneLine(sql)
        if len(result ) <=0 or result[1]  != '2':
            self.plog.output(" log_warings level shouble 2 now is  "+result[1], "ERROR")
            self.result["Defect"].append(
                {
                    'Desc': '错误日志等级没有设置恰当',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '配置 log_warnings 为 2',  # 修复建议
                }
            )
        self.plog.output("test error log level finish")

        sql = "SHOW DATABASES LIKE 'test';"
        result = self.getOneLine(sql)
        if len(result) > 0:
            self.plog.output("test DATABASE exits","ERROR")
            self.result["Defect"].append(
                {
                    'Desc': '测试数据库存在',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '尽快删除',  # 修复建议
                }
            )
        self.plog.output("test DATABASE check finish")


        sql = "SHOW VARIABLES WHERE Variable_name = 'local_infile';"
        result = self.getOneLine(sql)
        if len(result) > 0  and result[1] != "OFF":
            self.plog.output("local_infile is "+result[1],"ERROR")
            self.result["Defect"].append(
                {
                    'Desc': 'local_infile 可以 ',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '在mysql配置文件中新增一行：Local-infile=0；重启mysql',  # 修复建议
                }
            )
        self.plog.output("test local_infile check finish")


        sql = "SHOW variables LIKE 'have_symlink';"
        result = self.getOneLine(sql)
        if len(result) > 0  and result[1] != "YES":
            self.plog.output(" skip-symbolic-links  is "+result[1],"ERROR")
            self.result["Defect"].append(
                {
                    'Desc': ' skip-symbolic-links 开启可以防止数据库用户控制数据文件目录之外的文件。',  # 描述
                    'Level': '中',  # 危害等级
                    'Suggest': '在mysql配置文件中配置起启动',  # 修复建议
                }
            )
        self.plog.output("test skip-symbolic-links check finish")

        sql = "SELECT * FROM information_schema.plugins WHERE PLUGIN_NAME='daemon_memcached'"
        result = self.getOneLine(sql)
        if len(result) > 0  :
            self.plog.output(" information_schema.plugin  daemon_memcached  is  On ","ERROR")
            self.result["Defect"].append(
                {
                    'Desc': ' daemon_memcached 插件会导致数据泄漏。',  # 描述
                    'Level': '中',  # 危害等级
                    'Suggest': '执行 uninstall plugin daemon_memcached;',  # 修复建议
                }
            )
        self.plog.output("test daemon_memcached check finish")

        sql = "SHOW GLOBAL VARIABLES WHERE Variable_name = 'secure_file_priv' AND Value<>'';"
        result = self.getOneLine(sql)
        if len(result) <= 0  :
            self.plog.output(" secure_file_priv is off ","ERROR")
            self.result["Defect"].append(
                {
                    'Desc': ' secure_file_priv 限制客户端可以读取数据文件的路径。',  # 描述
                    'Level': '中',  # 危害等级
                    'Suggest': 'mysql配置文件中 添加 secure_file_priv=<path_to_load_directory>>;',  # 修复建议
                }
            )
        self.plog.output("test secure_file_priv check finish")


        sql = "SHOW VARIABLES LIKE 'sql_mode';"
        result = self.getOneLine(sql)
        if len(result)  > 0  and 'STRICT_TRANS_TABLES' not  in result[1] :
            self.plog.output(" sql_mode is  " +result[1]+" not safe ","ERROR")
            self.result["Defect"].append(
                {
                    'Desc': ' sql_mode 需要设置为 STRICT_ALL_TABLES ',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '配置文件添加 sql_mode=STRICT_ALL_TABLES',  # 修复建议
                }
            )
        self.plog.output("test sql_mode check finish")


        sql = "SHOW GLOBAL VARIABLES like 'disconnect_on_expired_password';"
        result = self.getOneLine(sql)
        if len(result)  > 0  and   result[1] != 'ON' :
            self.plog.output("disconnect_on_expired_password is  " +result[1]+" not safe ","ERROR")
            self.result["Defect"].append(
                {
                    'Desc': ' disconnect_on_expired_password  会导致过期账号依旧可以登陆数据库 ',  # 描述
                    'Level': '低',  # 危害等级
                    'Suggest': '配置文件添加 disconnect_on_expired_password =ON',  # 修复建议
                }
            )
        self.plog.output("test disconnect_on_expired_password check finish")

        pass

    def close(self):
        self.cursor.close()
        self.db.close()

    # DB helper func
    def getOneLine(self, sql):
        self.cursor.execute(sql)
        onedata = self.cursor.fetchone()
        if onedata == None:
            onedata = []
        return onedata

    def getAllLine(self,sql):
        self.cursor.execute(sql)
        onedata = self.cursor.fetchall()
        return  onedata

if __name__ == "__main__":
    mysq_test = mysql_baseline()
    mysq_test.runtest()
