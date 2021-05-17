import os
import shutil

from tools.models import Tools, DebugTalk
from tools.bin.models_visit import create_visit

from tools.debugtalk.utils import get_time_stamp
from tools.debugtalk.utils import dump_python_file
from tools.debugtalk import testcase


def get_talk_code(id):
    debugtalk_id = Tools.objects.get(id=id).debugtalk_id
    return DebugTalk.objects.get(id=debugtalk_id).debugtalk


def run(data, user_id):
    tool_id = data.get("tool_id")
    # 使用工具日志
    create_visit(data, user_id)

    variables = data.get("variables", dict())
    parame = data.get("params")
    if Tools.objects.filter(id=tool_id).exists():
        tool = Tools.objects.get(id=tool_id)
        base_dir_path = os.path.join(os.getcwd(), "tools/suite")
        base_dir_path = os.path.join(base_dir_path, get_time_stamp())

        talk_dir_path = os.path.join(base_dir_path, tool.card_router)
        full_path = talk_dir_path + '/debugtalk.py'

        if not os.path.exists(talk_dir_path):
            os.makedirs(talk_dir_path)

            try:
                debugtalk = get_talk_code(tool_id)
            except:
                debugtalk = ''
            dump_python_file(os.path.join(full_path), debugtalk)

        result = testcase.parse_parameters(parame, os.path.join(full_path), variables=variables)
        shutil.rmtree(base_dir_path)
        if result:
            return result
        return []
    return False
