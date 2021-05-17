from tools.models import Tools
from tools.models import Users
from tools.models import Project
from tools.models import DebugTalk
from tools.models import BackupDebugTalk
from tools.models import ToolVisitor

from django.forms.models import model_to_dict


def create_tool(data, user_id):
    image = data.get('image')
    card_router = data.get('card_router')
    name = data.get('name')
    describe = data.get('describe')
    params = data.get('params')
    function_meta = data.get('function_meta')
    project = data.get('project')
    debugtalk = data.get('debugtalk')

    tool_obj = Tools.objects
    obj_is_exists = tool_obj.filter(card_router=card_router).exists()
    if not obj_is_exists:
        debugtalk_obj = create_debugtalk(debugtalk, user_id)

        tool_obj.create(
            user_id=Users.objects.get(uid=user_id).uid,
            project_id=Project.objects.get(id=project.get('id')).id,
            debugtalk_id=DebugTalk.objects.get(id=debugtalk_obj.get('id')).id,
            name=name,
            image=image,
            card_router=card_router,
            describe=describe,
            params=params,
            function_meta=function_meta
        )
        return True
    return False


def update_tool(data, user_id):
    id = data.get('id')
    image = data.get('image')
    card_router = data.get('card_router')
    name = data.get('name')
    describe = data.get('describe')
    params = data.get('params')
    function_meta = data.get('function_meta')
    project = data.get('project')
    debugtalk = data.get('debugtalk')

    tool_obj = Tools.objects
    if tool_obj.filter(id=id).exists():
        tool = tool_obj.get(id=id)
        tool.image = image
        tool.card_router = card_router
        tool.name = name
        tool.describe = describe
        tool.params = params
        tool.function_meta = function_meta
        tool.project_id = Project.objects.get(id=project.get('id')).id
        tool.save()

        update_debugtalk(debugtalk, user_id)
        return True
    return False


def get_tool(tool_id):
    if Tools.objects.filter(id=tool_id).exists():
        tool = Tools.objects.get(id=tool_id)
        tool_dict = model_to_dict(tool)
        tool_dict['update_time'] = tool.update_time.strftime('%Y-%m-%d %H:%M:%S')
        tool_dict['create_time'] = tool.create_time.strftime('%Y-%m-%d %H:%M:%S')
        tool_dict['params'] = eval(tool.params)
        tool_dict['function_meta'] = eval(tool.function_meta)
        tool_dict['project'] = model_to_dict(Project.objects.get(id=tool.project_id))
        tool_dict['debugtalk'] = get_debugtalk(tool.debugtalk_id)
        tool_dict['user'] = model_to_dict(Users.objects.get(uid=tool.user_id))
        return tool_dict
    else:
        return False


def get_tools():
    tools_list = list()
    all_dict = {
        'id': 0,
        'name': 'all',
        'label': '所有',
        'tools': []
    }
    for tool in Tools.objects.filter(state=1).order_by('-sort'):
        tools_dict = model_to_dict(tool)
        tools_dict['project'] = model_to_dict(Project.objects.get(id=tool.project_id))
        tools_dict['visit_sum'] = ToolVisitor.objects.filter(tool_id=tool.id).count()
        all_dict['tools'].append(tools_dict)

    tools_list.append(all_dict)
    projects = Project.objects.filter(state=1).order_by('-sort')
    for project in projects:
        project_dict = dict()
        project_dict['id'] = project.id
        project_dict['name'] = project.name
        project_dict['label'] = project.label
        project_dict['tools'] = []
        for tool in Tools.objects.filter(project_id=project.id, state=1).order_by('-sort'):
            tools_dict = model_to_dict(tool)
            tools_dict['project'] = model_to_dict(Project.objects.get(id=tool.project_id))
            tools_dict['visit_sum'] = ToolVisitor.objects.filter(tool_id=tool.id).count()
            project_dict['tools'].append(tools_dict)
        tools_list.append(project_dict)
    return tools_list


def delete_tool(tool_id):
    if Tools.objects.filter(id=tool_id).exists():
        tool = Tools.objects.get(id=tool_id)
        tool.state = 0
        tool.save()
        return True
    return False


def create_debugtalk(data, user_id):
    debugtalk = data.get('debugtalk', '')
    data = DebugTalk.objects.create(
        user_id=Users.objects.get(uid=user_id).uid,
        debugtalk=debugtalk
    )
    return model_to_dict(DebugTalk.objects.get(id=data.id))


def get_debugtalk(id):
    if DebugTalk.objects.filter(id=id).exists():
        return model_to_dict(DebugTalk.objects.get(id=id))
    return False


def update_debugtalk(data, user_id):
    id = data.get('id')
    debugtalk = data.get('debugtalk')

    debugtalk_obj = DebugTalk.objects
    is_exists = debugtalk_obj.filter(id=id).exists()
    if is_exists:
        info = debugtalk_obj.get(id=id)
        info.debugtalk = debugtalk
        info.save()
        BackupDebugTalk.objects.create(
            debugtalk_id=debugtalk_obj.get(id=id).id,
            user_id=Users.objects.get(uid=user_id).uid,
            backup_debugtalk=debugtalk
        )
        return True
    return False
