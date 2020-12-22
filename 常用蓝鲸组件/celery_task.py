from celery.schedules import crontab
from celery.task import periodic_task, task

from blueapps.utils.logger import logger_celery
from home_application.models import Operation
from home_application.service.bk_service import BkService


@periodic_task(run_every=crontab(minute='0', hour='1', day_of_week='*', day_of_month='*', month_of_year='*'),
               name="demo")
def demo():
    logger_celery.info('demo')


@task()
def execute_job(**kwargs):
    logger_celery.info("kwargs:{}".format(kwargs))
    username = kwargs.get('username')
    bk_service = BkService(username=username)
    info = bk_service.execute_job(**kwargs)
    logger_celery.info("execute_job=>{}".format(info))
    job_instance_id = info.get('data').get('job_instance_id')
    job_kwargs = {
        'bk_biz_id': kwargs.get('bk_biz_id'),
        'job_instance_id': job_instance_id
    }
    job_status = bk_service.get_job_instance_status(**job_kwargs)
    logger_celery.info("get_job_instance_status=>{}".format(job_status))
    if job_status.get('result'):
        log_info = bk_service.get_job_instance_log(**job_kwargs)
        logger_celery.info("get_job_instance_log=>{}".format(log_info))
        if log_info.get('result'):
            log_datas = log_info.get('data')
            for log_data in log_datas:
                if log_data.get('is_finished'):
                    log_step_results = log_data.get('step_results')
                    for log_step_result in log_step_results:
                        ip_logs = log_step_result.get('ip_logs')
                        for ip_log in ip_logs:
                            opt = Operation()
                            opt.user = username
                            opt.biz = kwargs.get('bk_biz_id')
                            opt.machine_list = ip_log.get('ip')
                            opt.result = log_step_result.get('ip_status')
                            opt.log = ip_log.get('log_content')
                            opt.save()
