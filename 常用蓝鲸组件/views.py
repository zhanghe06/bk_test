# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import json

from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from blueapps.account.decorators import login_exempt
from home_application import celery_task
from home_application.bo.BkPageManager import BkPageManage
from home_application.bo.form import JobForm
from home_application.models import Script, Operation
from home_application.service.bk_service import BkService


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, "home_application/index_home.html")


def dev_guide(request):
    """
    开发指引
    """
    return render(request, "home_application/dev_guide.html")


def contact(request):
    """
    联系页
    """
    return render(request, "home_application/contact.html")


def get_user(request):
    result = {'result': True, 'user_name': request.user.username}
    return JsonResponse(result)


def search_business(request):
    bk_service = BkService(request=request)
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    no_page = bool(request.GET.get('no_page', False))
    bk_page = BkPageManage(func=bk_service.search_business, page=page, limit=page_size, no_page=no_page)()
    result, count = bk_page.get_result()
    data = {
        'total': count,
        'data': result
    }
    return JsonResponse(data)


def search_set(request):
    bk_service = BkService(request=request)
    bk_biz_id = request.GET.get('bk_biz_id', 0)
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    no_page = bool(request.GET.get('no_page', False))
    kwargs = {
        'bk_biz_id': bk_biz_id
    }
    bk_page = BkPageManage(func=bk_service.search_set, page=page, limit=page_size, no_page=no_page, **kwargs)()
    result, count = bk_page.get_result()
    data = {
        'total': count,
        'data': result
    }
    return JsonResponse(data)


def search_module(request):
    bk_service = BkService(request=request)
    bk_biz_id = request.GET.get('bk_biz_id', 0)
    bk_set_id = request.GET.get('bk_set_id', 0)
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    no_page = bool(request.GET.get('no_page', False))
    kwargs = {
        'bk_biz_id': bk_biz_id,
        'bk_set_id': bk_set_id
    }
    bk_page = BkPageManage(func=bk_service.search_module, page=page, limit=page_size, no_page=no_page, **kwargs)()
    result, count = bk_page.get_result()
    data = {
        'total': count,
        'data': result
    }
    return JsonResponse(data)


@require_http_methods(["POST", "GET"])
def search_host(request):
    bk_service = BkService(request=request)
    body = request.body
    body = json.loads(request.body) if body else {}
    page = int(body.get('page', 1))
    page_size = int(body.get('page_size', 10))
    no_page = bool(body.get('no_page', False))
    bk_biz_id = body.get('bk_biz_id', 0)
    bk_set_id = body.get('bk_set_id', 0)
    bk_module_id = body.get('bk_module_id', 0)
    ip = list(body.get('ip', []))
    kwargs = {
        'condition': [
            {
                "bk_obj_id": "host",
                "fields": ['bk_host_name', 'bk_host_innerip', 'bk_host_outerip'],
                "condition": []
            },
            {
                "bk_obj_id": "biz",
                "fields": ['bk_biz_id', 'bk_biz_name'],
                "condition": []
            },
            {
                "bk_obj_id": "set",
                "fields": ['bk_set_id', 'bk_set_name'],
                "condition": []
            },
            {
                "bk_obj_id": "module",
                "fields": ["bk_module_id", 'bk_module_name'],
                "condition": []
            }
        ]
    }
    if bk_biz_id:
        kwargs.update({
            'bk_biz_id': bk_biz_id,
        })
    if bk_set_id:
        kwargs.get('condition')[2] = {
            "bk_obj_id": "set",
            "fields": ['bk_set_id', 'bk_set_name'],
            "condition": [
                {
                    "field": "bk_set_id",
                    "operator": "$eq",
                    "value": bk_set_id
                }
            ]
        }
    if bk_module_id:
        kwargs.get('condition')[3] = {
            "bk_obj_id": "module",
            "fields": ['bk_module_id', 'bk_module_name'],
            "condition": [
                {
                    "field": "bk_module_id",
                    "operator": "$eq",
                    "value": bk_module_id
                }
            ]
        }
    if ip:
        kwargs.update(
            {
                "ip": {
                    "data": ip,
                    "exact": 1,
                    "flag": "bk_host_innerip|bk_host_outerip"
                },
            }
        )
    bk_page = BkPageManage(func=bk_service.search_host, page=page, limit=page_size, no_page=no_page, **kwargs)()
    result, count = bk_page.get_result()
    data = {
        'total': count,
        'data': result
    }
    return JsonResponse(data)


@require_http_methods(["POST", "GET"])
@login_exempt
@csrf_exempt
def search_script(request):
    body = request.body
    body = json.loads(request.body) if body else {}
    page = int(body.get('page', 1))
    page_size = int(body.get('page_size', 10))
    query_set = Script.objects.all()
    paginate = Paginator(query_set, page_size)
    page_list = paginate.page(page)
    res = json.loads(serializers.serialize('json', page_list))
    total = paginate.count
    data = {
        "total": total,
        "data": res
    }
    return JsonResponse(data, safe=False)


def create_task(request):
    bk_service = BkService(request=request)
    kwargs = {
        'bk_biz_id': 2
    }
    info = bk_service.create_task(**kwargs)
    return JsonResponse(info)


@require_http_methods(["POST"])
def execute_job(request):
    bk_service = BkService(request=request)
    body = request.body
    body = json.loads(request.body) if body else {}
    job_form = JobForm(body)
    if not job_form.is_valid():
        return JsonResponse(job_form.get_errors())
    bk_biz_id = job_form.cleaned_data.get('bk_biz_id')
    bk_job_id = job_form.cleaned_data.get('bk_job_id')
    kwargs = {
        'username': request.user.username,
        'bk_biz_id': bk_biz_id,
        'bk_job_id': bk_job_id
    }
    job_detail = bk_service.get_job_detail(**kwargs)
    steps = job_detail.get('data').get('steps')
    for step in steps:
        step['ip_list'] = body.get('ip_list')
    kwargs.update({
        'steps': steps
    })
    celery_task.execute_job.delay(**kwargs)
    return JsonResponse({'result': True})


@require_http_methods(["POST", "GET"])
@login_exempt
@csrf_exempt
def search_operation(request):
    body = request.body
    body = json.loads(request.body) if body else {}
    page = int(body.get('page', 1))
    page_size = int(body.get('page_size', 10))
    query_set = Operation.objects.all()
    paginate = Paginator(query_set, page_size)
    page_list = paginate.page(page)
    res = json.loads(serializers.serialize('json', page_list))
    total = paginate.count
    data = {
        "total": total,
        "data": res
    }
    return JsonResponse(data, safe=False)
