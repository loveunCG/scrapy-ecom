import os
import django
import sys
sys.path.append(os.path.dirname(os.path.abspath('.')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopifycheckout.settings")
django.setup()
from shopify.utils import TaskStatus

from API.models import Profile
from API.models import Task
from API.models import Checkout
from API.models import Proxies


def get_profile():
    pass
    return Profile

def set_profile(profile):
    pass
    return profile

def get_queued_task():
    try:
        task = Task.objects.filter(status=TaskStatus.QUEUED).order_by('id')[0]
    except Task.DoesNotExist:
        task = False
    return task


def get_researching_task():
    try:
        task = Task.objects.filter(status=TaskStatus.RESEARCH).order_by('id')[0]
    except Task.DoesNotExist:
        task = False
    return task

def update_task_status(task, status):
    print('-----update status-------')
    try:
        task.update(status = status)
        return True
    except Exception as e:
        return False

def set_no_search_result(task):
    try:
        task.update(status = TaskStatus.NOSEARCHRESULT)
        return True
    except Exception as e:
        return False
