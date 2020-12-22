from time import sleep

from blueapps.utils.logger import logger_celery
from blueking.component.shortcuts import get_client_by_user, get_client_by_request


class BkService(object):
    def __init__(self, username='admin', request=None):
        self.count = 0
        if request:
            self.client = get_client_by_request(request)
        else:
            self.client = get_client_by_user(username)

    def search_business(self, **kwargs):
        info = self.client.cc.search_business(kwargs)
        if info.get('result'):
            return info.get('data').get('info'), info.get('data').get('count')
        else:
            return [], 0

    def search_host(self, **kwargs):
        info = self.client.cc.search_host(kwargs)
        if info.get('result'):
            return info.get('data').get('info'), info.get('data').get('count')
        else:
            return [], 0

    def create_task(self, **kwargs):
        info = self.client.sops.get_template_list(kwargs)
        return info

    def search_set(self, **kwargs):
        info = self.client.cc.search_set(kwargs)
        if info.get('result'):
            return info.get('data').get('info'), info.get('data').get('count')
        else:
            return [], 0

    def search_module(self, **kwargs):
        info = self.client.cc.search_module(kwargs)
        if info.get('result'):
            return info.get('data').get('info'), info.get('data').get('count')
        else:
            return [], 0

    def execute_job(self, **kwargs):
        info = self.client.job.execute_job(kwargs)
        return info

    def get_job_instance_log(self, **kwargs):
        info = self.client.job.get_job_instance_log(kwargs)
        return info

    def get_job_instance_status(self, **kwargs):
        info = self.client.job.get_job_instance_status(kwargs)
        self.count += 1
        logger_celery.info(self.count.__add__(1))
        if self.count == 240:
            return info
        result = info.get('result')
        if result:
            data = info.get('data')
            is_finished = data.get('is_finished')
            if not is_finished:
                sleep(1)
                self.get_job_instance_status(**kwargs)
        self.count = 0
        return info

    def get_job_detail(self, **kwargs):
        info = self.client.job.get_job_detail(kwargs)
        return info
