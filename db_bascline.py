# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from script.mysql_baseline import *
from loghandle import *
import getopt

if __name__ == "__main__":
    bannber = '''
 ____  ____  ____                 _ _       {''' + db_baseline_basic.getVersion() + '''}
|  _ \| __ )| __ )  __ _ ___  ___| (_)_ __   ___
| | | |  _ \|  _ \ / _` / __|/ _ \ | | '_ \ / _ \\
| |_| | |_) | |_) | (_| \__ \  __/ | | | | |  __/
|____/|____/|____/ \__,_|___/\___|_|_|_| |_|\___|
       (https://github.com/wstart/DB_BaseLine)
--------------------------------------------------'''

    supperdb = ["mysql"]
    DBnames = ",".join(supperdb)
    small_helper='''
Usage: python db_baseline.py  [options]
       python db_baseline.py -h for more infomation
    '''
    helper = '''
Usage: python db_baseline.py [options]

[Options]:
    -v ,--version show version

    -h,--help  show help

    -D,--database   check DataBase type,default is mysql
                    support Database list: ''' + DBnames + '''

    -H,--host   host,Default:127.0.0.1
                if host is not 127.0.0.1 or localhost only check command

    -P,--database-port   database port,Default:Database Default port
                         it will set by check script

    -u,--database-user  database rootuser,default:root

    -p,--database-password   database password,default:root

    '''

    plog = loghandle.getLogEntity()

    plog.output(bannber, "INFO", showtime=False, showlevel=False)

    runconfig = {
        "database": "",
        "host": "",
        "database_port": "",
        "database_user": "",
        "database_password": ""
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhD:H:P:u:p:",
                                   ["version", "help", "database=", "host=", "database-port=", "database-user=",
                                    "database-password="])

        checkscript = ""
        if len(opts) == 0:
            print small_helper
            exit()

        for o, a in opts:
            if o in ("-v", "--version"):
                print("DB_BASELINE : " + db_baseline_basic.getVersion())
                sys.exit()
            elif o in ("-h", "--help"):
                print helper
                sys.exit()
            elif o in ("-D", "--database"):
                runconfig["database"] = a
            elif o in ("-H", "--host"):
                runconfig["host"] = a
            elif o in ("-P", "--database-port"):
                runconfig["database_port"] = a
            elif o in ("-U", "--database-user"):
                runconfig["database_user"] = a
            elif o in ("-p", "--database-password"):
                runconfig["database_password"] = a

        if runconfig["database"] == "mysql":
            checkscript = mysql_baseline(runconfig)

        if checkscript != "":
            result = checkscript.runtest()

        else:
            plog.output("No match DataBase Type","ERROR")
            print  small_helper
            plog.output("DBBaseline exit()")
    except getopt.GetoptError:
        print helper
