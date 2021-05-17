# from django.shortcuts import render
import traceback
from django.http import JsonResponse, HttpResponse

from tools.bin import models_project
from tools.bin import models_user
from tools.bin import models_tools
from tools.bin import models_wisdom
from tools.bin import models_visit
from tools.bin import models_logs
from tools.bin import models_run
from tools.bin import models_nav

from tools.utils.lark_login import Access
from tools.utils.public import body_to_dict
from tools.utils.public import response_json


def project(request):
    response = response_json()
    try:
        if request.method == "GET":
            project_list = models_project.get_all_class()
            response['data'] = project_list
            return JsonResponse(response)

        if request.method == "POST":
            data = body_to_dict(request)
            result = models_project.create_class(data)
            if result:
                response['message'] = '创建成功'
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = "定义的URL已存在"
            return JsonResponse(response)

        if request.method == "PUT":
            data = body_to_dict(request)
            result = models_project.update_class(data)
            if result:
                response['extra'] = result
                return JsonResponse(response)
            response['code'] = 402
            response['message'] = "未找到"
            return JsonResponse(response)

        if request.method == "DELETE":
            data = body_to_dict(request)
            result = models_project.delete_class(data)
            if result:
                response['message'] = "删除成功"
                return JsonResponse(response)
            response['code'] = 403
            response['message'] = "未找到"
            return JsonResponse(response)

    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def user(request):
    response = response_json()
    try:
        if request.method == "GET":
            code = request.GET.get('code', '')
            user_info = Access(code).get_user_info()
            response['extra'] = user_info
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def user_info(request):
    response = response_json()
    try:
        if request.method == "GET":
            user_id = request.GET.get('user_id', '')
            user_info = models_user.get_user_info(user_id)
            if user_info is not False:
                response['extra'] = user_info
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = '未找到'
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def users(request):
    response = response_json()
    try:
        if request.method == "GET":
            user_info = models_user.get_users()
            response['data'] = user_info
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def tool(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            result = models_tools.create_tool(data, user_id)
            if result:
                response['message'] = '创建成功'
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = "虚拟路由已存在，请重新定义。"
            return JsonResponse(response)

        if request.method == "GET":
            tool_id = request.GET.get('tool_id', None)
            result = models_tools.get_tool(tool_id)
            if result:
                response['extra'] = result
                return JsonResponse(response)
            response['code'] = 402
            response['message'] = '未找到'
            return JsonResponse(response)

        if request.method == "PUT":
            data = body_to_dict(request)
            result = models_tools.update_tool(data, user_id)
            if result:
                response['message'] = '更新成功'
                return JsonResponse(response)
            response['code'] = 403
            response['message'] = '未找到'
            return JsonResponse(response)

        if request.method == "DELETE":
            data = body_to_dict(request)
            result = models_tools.delete_tool(data.get('id'))
            if result:
                response['message'] = '删除成功'
                return JsonResponse(response)
            response['code'] = 405
            response['message'] = '未找到'
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def tools(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "GET":
            result = models_tools.get_tools()
            if result:
                response['data'] = result
                return JsonResponse(response)
            response['code'] = 402
            response['message'] = '未找到'
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def debugtalk(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            result = models_tools.create_debugtalk(data, user_id)
            response['message'] = '创建成功'
            response['extra'] = result
            return JsonResponse(response)

        if request.method == "PUT":
            data = body_to_dict(request)
            result = models_tools.update_debugtalk(data, user_id)
            if result:
                response['message'] = '更新成功'
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = 'debugtalk不存在'
            return JsonResponse(response)

        if request.method == 'GET':
            id = request.GET.get('id')
            result = models_tools.get_debugtalk(id)
            if result:
                response['extra'] = result
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = 'debugtalk不存在'
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def launch(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            result = models_run.run(data, user_id)
            if result:
                response['data'] = result
                return JsonResponse(response)
            response['message'] = '无响应信息'
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def wisdom(request):
    response = response_json()
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            models_wisdom.create_wisdom(data)
            response['message'] = '创建成功'
            return JsonResponse(response)

        if request.method == "GET":
            result = models_wisdom.get_wisdom()
            response['extra'] = result
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def visit(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            models_visit.create_visit(data, user_id)
            response['message'] = '创建成功'
            return JsonResponse(response)

        if request.method == "GET":
            tool_id = request.GET.get('tool_id', None)
            project_id = request.GET.get('project_id', None)
            user_id = request.headers.get('uid', None)
            result = models_visit.get_visit(tool_id=tool_id, project_id=project_id, user_id=user_id)
            response['extra'] = {'count': result}
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def viewer(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "GET":
            tool_id = request.GET.get('tool_id', None)
            result = models_visit.get_viewer(tool_id=tool_id)
            response['data'] = result
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def logs(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            models_logs.create_log(data, user_id)
            response['message'] = '创建成功'
            return JsonResponse(response)

        if request.method == "GET":
            event = request.GET.get('event')
            result = models_logs.get_logs(user_id, event)
            if result:
                response['data'] = result
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = '未找到'
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def kind(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            models_nav.create_kind(data)
            response['message'] = '创建成功'
            return JsonResponse(response)

        if request.method == "PUT":
            data = body_to_dict(request)
            result = models_nav.update_kind(data)
            if result:
                response['message'] = '更新成功'
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = '未找到'
            return JsonResponse(response)

        if request.method == "DELETE":
            data = body_to_dict(request)
            models_nav.delete_kind(data)
            response['message'] = '成功'
            return JsonResponse(response)

        if request.method == "GET":
            result = models_nav.get_kinds()
            response['data'] = result
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def navigations(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "GET":
            result = models_nav.get_navigations()
            response['data'] = result
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def navigation(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            models_nav.creat_nav(data)
            response['message'] = '创建成功'
            return JsonResponse(response)

        if request.method == "PUT":
            data = body_to_dict(request)
            result = models_nav.update_nav(data)
            if result:
                response['message'] = '更新成功'
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = '未找到'
            return JsonResponse(response)

        if request.method == "DELETE":
            data = body_to_dict(request)
            result = models_nav.delete_nav(data)
            if result:
                response['message'] = '删除成功'
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = '未找到'
            return JsonResponse(response)

        if request.method == "GET":
            result = models_nav.get_navs()
            response['data'] = result
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)


def demo(request):
    response = response_json()
    user_id = request.headers.get('uid')
    try:
        if request.method == "POST":
            data = body_to_dict(request)
            response['message'] = '创建成功'
            return JsonResponse(response)

        if request.method == "PUT":
            data = body_to_dict(request)
            response['message'] = '更新成功'
            return JsonResponse(response)

        if request.method == "DELETE":
            data = body_to_dict(request)
            response['message'] = '删除成功'
            return JsonResponse(response)

        if request.method == "GET":
            event = request.GET.get('event')
            result = models_logs.get_logs(user_id, event)
            if result:
                response['data'] = result
                return JsonResponse(response)
            response['code'] = 401
            response['message'] = '未找到'
            return JsonResponse(response)
    except:
        response['code'] = 500
        response['message'] = traceback.format_exc()
        return JsonResponse(response)
