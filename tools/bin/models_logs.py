from tools.models import Users
from tools.models import Logs
from django.forms.models import model_to_dict


def create_log(data, user_id):
    event = data.get('event')
    content = data.get('content')
    Logs.objects.create(user_id=user_id, event=event, content=content)


def get_logs(user_id, event):
    log_list = list()
    is_exists = Users.objects.filter(uid=user_id).exists()
    if is_exists:
        logs = Logs.objects.filter(user_id=user_id, event=event).order_by('-id')[:10]
        for log in logs:
            log_list.append(model_to_dict(log))
        return log_list
    return False
