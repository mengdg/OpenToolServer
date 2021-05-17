from tools.models import Tools
from tools.models import Navigation
from tools.models import Kind

from django.forms.models import model_to_dict


def create_kind(data):
    name = data.get('name')
    Kind.objects.create(name=name)


def update_kind(data):
    id = data.get('id')
    name = data.get('name')
    sort = data.get('sort')
    if Kind.objects.filter(id=id).exists():
        kind_obj = Kind.objects.get(id=id)
        kind_obj.name = name
        kind_obj.sort = sort
        kind_obj.save()
        return True
    return False


def delete_kind(data):
    id = data.get('id')
    kind_obj = Kind.objects.get(id=id)
    if kind_obj.state == 1:
        kind_obj.state = 0
    else:
        kind_obj.state = 1
    kind_obj.save()


def get_kinds():
    kind_obj = Kind.objects.filter().order_by('-sort')
    return [model_to_dict(kind) for kind in kind_obj]


def creat_nav(data):
    name = data.get('name')
    url = data.get('url')
    img = data.get('img')
    desc = data.get('desc')
    kind_id = data.get('kind_id')
    recommend = data.get('recommend')
    sort = data.get('sort')
    Navigation.objects.create(
        name=name,
        url=url,
        img=img,
        desc=desc,
        kind_id=Kind.objects.get(id=kind_id).id,
        recommend=recommend,
        sort=sort
    )


def update_nav(data):
    id = data.get('id')
    name = data.get('name')
    url = data.get('url')
    img = data.get('img')
    desc = data.get('desc')
    kind_id = data.get('kind_id')
    recommend = data.get('recommend')
    sort = data.get('sort')
    nav_obj = Navigation.objects
    if nav_obj.filter(id=id).exists():
        nav = nav_obj.get(id=id)
        nav.name = name
        nav.url = url
        nav.img = img
        nav.desc = desc
        nav.kind_id = Kind.objects.get(id=kind_id).id
        nav.recommend = recommend
        nav.sort = sort
        nav.save()
        return True
    return False


def delete_nav(data):
    id = data.get('id')
    nav_obj = Navigation.objects
    if nav_obj.filter(id=id).exists():
        nav = nav_obj.get(id=id)
        if nav.state == 1:
            nav.state = 0
        else:
            nav.state = 1
        nav.save()
        return True
    return False


def get_navs():
    kins = get_kinds()
    nav_obj = Navigation.objects
    navs_list = list()

    recommends = nav_obj.filter(state=1, recommend=1)
    recommend_list = list()
    for recommend in recommends:
        recommend_dict = model_to_dict(recommend)
        recommend_dict['kind'] = model_to_dict(Kind.objects.get(id=recommend.kind_id))
        recommend_list.append(recommend_dict)
    if len(recommend_list) > 0:
        navs_list.append({'id': 0, 'name': '推荐应用', 'navs': recommend_list})

    for kind in kins:
        navs_dict = dict()
        navs = nav_obj.filter(state=1, kind_id=Kind.objects.get(id=kind.get('id'))).order_by('-sort')
        nav_list = list()
        for nav in navs:
            nav_dict = model_to_dict(nav)
            nav_list.append(nav_dict)
        if len(nav_list) > 0:
            navs_dict['id'] = kind.get('id')
            navs_dict['name'] = kind.get('name')
            navs_dict['navs'] = nav_list
            navs_list.append(navs_dict)
    return navs_list


def get_navigations():
    nav_obj = Navigation.objects
    kind_obj = Kind.objects
    navs_list = list()
    navs = nav_obj.filter()
    for nav in navs:
        nav_dict = model_to_dict(nav)
        nav_dict['kind'] = model_to_dict(kind_obj.get(id=nav.kind_id))
        nav_dict['kind_id'] = nav.kind_id
        navs_list.append(nav_dict)
    return navs_list
