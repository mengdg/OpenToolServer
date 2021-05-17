from tools.models import Project

from django.forms.models import model_to_dict


def create_class(data):
    name = data.get('name')
    label = data.get('label')
    sort = data.get('sort')
    class_obj = Project.objects
    obj_is_exists = class_obj.filter(name=name).exists()
    if not obj_is_exists:
        class_obj.create(name=name, label=label, sort=sort)
        return True
    return False


def get_all_class():
    class_list = list()
    all_class_obj = Project.objects.all().filter().order_by('-sort')
    for obj in all_class_obj: class_list.append(model_to_dict(obj))
    return class_list


def update_class(data):
    id = data.get('id')
    name = data.get('name')
    label = data.get('label')
    sort = data.get('sort', None)
    class_obj = Project.objects
    info = class_obj.get(id=id)
    if class_obj.filter(id=id).exists():
        info.name = name
        info.label = label
        if sort is not None:
            info.sort = sort
        info.save()
        return model_to_dict(info)
    return False


def delete_class(data):
    id = data.get('id')
    class_obj = Project.objects
    info = class_obj.get(id=id)
    if class_obj.exists():
        if info.state == 1:
            info.state = 0
        else:
            info.state = 1
        info.save()
        return True
    return False
