from tools.models import Users
from tools.models import Tools
from tools.models import ToolVisitor

from django.forms.models import model_to_dict
from django.db.models import Count


def create_visit(data, user_id):
    tool_id = data.get('tool_id')
    if Users.objects.filter(uid=user_id).exists() and Tools.objects.filter(id=tool_id).exists():
        ToolVisitor.objects.create(
            user_id=Users.objects.get(uid=user_id).uid,
            tool_id=Tools.objects.get(id=tool_id).id
        )
        return True
    return False


def get_visit(tool_id=None, project_id=None, user_id=None):
    num = 0
    # 单个项目所有工具的查看次数
    if project_id is not None and tool_id is None and user_id is None:
        tools = Tools.objects.filter(project_id=project_id)
        for tool in tools:
            count = ToolVisitor.objects.filter(tool_id=tool.id).count()
            num += count
        return num
    # 单个工具所有查询次数
    elif tool_id is not None and project_id is None and user_id is None:
        count = ToolVisitor.objects.filter(tool_id=tool_id).count()
        return count
    # 单个用户所有工具使用次数
    elif user_id is not None and project_id is None and tool_id is None:
        count = ToolVisitor.objects.filter(user_id=user_id).count()
        return count
    # 单个用户单个项目使用次数
    elif user_id is not None and project_id is not None and tool_id is None:
        tools = Tools.objects.filter(project_id=project_id)
        for tool in tools:
            count = ToolVisitor.objects.filter(user_id=user_id, tool_id=tool.id).count()
            num += count
        return num
    # 单个用户单个工具使用次数
    elif user_id is not None and tool_id is not None and project_id is None:
        tool = Tools.objects.get(id=tool_id)
        count = ToolVisitor.objects.filter(user_id=user_id, tool_id=tool.id).count()
        return count
    # 所有查看次数
    else:
        return ToolVisitor.objects.count()


def get_viewer(tool_id):
    view_list = list()
    distinct = []
    user_obj = Users.objects
    view_obj = ToolVisitor.objects.filter(tool_id=tool_id).order_by('-id')
    for view in view_obj:
        if view.user_id in distinct:
            continue
        if len(distinct) > 10:
            return view_list
        distinct.append(view.user_id)
        view_dict = model_to_dict(view)
        view_dict['create_time'] = view.create_time.strftime('%Y-%m-%d %H:%M:%S')
        view_dict['user'] = model_to_dict(user_obj.get(uid=view.user_id))
        view_list.append(view_dict)
    return view_list
