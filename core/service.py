from core.models import *
from api.serializers import *
import requests


def send_task(task: EventTask):
    data = {
        'tg_id': task.event_user.user.tg_id,
        'task': EventTaskSerializer(task).data
    }
    response = requests.post(url='https://de22-178-205-174-86.ngrok-free.app/new_task', json=data)

    return response.status_code

