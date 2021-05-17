from tools.models import Wisdom

from django.forms.models import model_to_dict
import random


def create_wisdom(data):
    text = data.get('text')
    Wisdom.objects.create(text=text)


def get_wisdom():
    count = Wisdom.objects.count()
    if count > 0:
        random_id = random.randint(1, count)
        text_obj = Wisdom.objects.get(id=random_id)
        return model_to_dict(text_obj)
    return {'text': '哎哟。。。哀家已经词穷才进了，赶紧棒棒哀家！！！'}
