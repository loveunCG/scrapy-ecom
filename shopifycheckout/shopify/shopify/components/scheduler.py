import random
import time
from shopify.components.gateway import get_queued_task, get_researching_task


class Scheduler():

    @staticmethod
    def __waiting_for_no_result__():
        while True:
            task = get_researching_task()
            if task is not False:
                break
            time.sleep(5)
        return task

    @staticmethod
    def __waiting_for_active_task__():
        task = get_queued_task()
        while True:
            if task is not False:
                break
            time.sleep(5)
        return task
