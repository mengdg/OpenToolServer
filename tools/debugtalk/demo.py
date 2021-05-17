import MySQLdb as mdb
import os
from tools.debugtalk.utils import get_time_stamp
from tools.debugtalk.utils import dump_python_file
from tools.debugtalk import testcase


# 获取代码
def get_talk_code(id):
    con = mdb.connect('10.9.128.47', 'root', 'qatest', 'HttpRunner', charset='utf8')
    # 使用cursor()方法获取操作游标
    cur = con.cursor()
    cur.execute("select debugtalk from DebugTalk where id=%d;" % int(id))
    result = cur.fetchone()
    cur.close()
    return result


def save_talk():
    base_dir_path = os.path.join(os.getcwd(), "suite")
    base_dir_path = os.path.join(base_dir_path, get_time_stamp())

    talk_dir_path = os.path.join(base_dir_path, '测试')

    if not os.path.exists(talk_dir_path):
        os.makedirs(talk_dir_path)

        try:
            debugtalk = get_talk_code(4)[0]
        except:
            debugtalk = ''
        dump_python_file(os.path.join(talk_dir_path, 'debugtalk.py'), debugtalk)

    parame = [
        {"app": "${get_UA($version)}"}
    ]
    test = testcase.parse_parameters(parame, os.path.join(talk_dir_path, 'debugtalk.py'), variables={"version": "2.1.1"})
    print(test)


save_talk()
