from tools.models import Users

from django.forms.models import model_to_dict


def get_user(data):
    uid = data.get('open_id')
    user_obj = Users.objects
    is_exists = user_obj.all().filter(uid=uid).exists()
    if not is_exists:
        user_obj.create(
            uid=data.get('open_id'),
            name=data.get('name'),
            mobile=data.get('mobile', ''),
            email=data.get('email', ''),
            avatar=data.get('avatar_big'),
            state=1,
            identity=['viewer']
        )
    info = user_obj.all().filter(uid=uid).first()
    result = model_to_dict(info)
    result['identity'] = eval(info.identity)
    return result


def get_user_info(user_id):
    if Users.objects.filter(uid=user_id).exists():
        info_obj = Users.objects.get(uid=user_id)
        user_dict = model_to_dict(info_obj)
        user_dict['identity'] = eval(info_obj.identity)
        return user_dict
    return False


def get_users():
    user_obj = Users.objects
    all_users = user_obj.all()
    users_list = list()
    for user in all_users:
        user_dict = model_to_dict(user)
        user_dict['identity'] = eval(user.identity)
        users_list.append(user_dict)
    return users_list
