from datetime import datetime

from core.models import *
from api.serializers import *
import requests

bot_url = 'https://bot.events.fvds.ru/'


def send_new_task(task: EventTask):
    data = {
        'tg_id': task.event_user.user.tg_id,
        'task': EventTaskSerializer(task).data
    }
    response = requests.post(url=bot_url + 'new_task', json=data)

    return response.status_code


def send_task_result(task: EventTask):
    data = {
        'tg_id': task.event_user.user.tg_id,
        'task': EventTaskSerializer(task).data
    }

    response = requests.post(url=bot_url + 'task', json=data)

    return response.status_code
