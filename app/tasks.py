import os
import requests
from urllib3.contrib import pyopenssl as reqs
from datetime import datetime, timedelta

from zdjc.celery import app
from utils import tools
from .models import Site, SiteHistory

from django.template.loader import render_to_string
from django.db import connection

from celery.task.schedules import crontab
from celery.decorators import periodic_task


# def process_code_info(site_history):
#     code = site_history.site_type
#     if code == '2':
#         code_info = '证书即将过期:%s天后过期'%(site_history.certificate)
#     elif code == '3':
#         code_info = '状态码：%s'%(site_history.status_code)
#     elif code == '4':
#         code_info = '访问超时%s'%site_history.ping_time
#     else:
#         code_info = '访问异常'

#     return code_info


# def send_msg_to_wx(bad_sites=None, day_task=False):
#     if bad_sites:
#         title = "站点每日情况-存在异常" if day_task else '发现异常站点'
#         sites_info = ["[{name}]({href}) {code}".format(name=each.site.name, 
#                             href="http://"+each.site.href, code=process_code_info(each)) \
#                             for each in bad_sites]
#         sites_info.insert(0, title)
#     else:
#         title = "站点每日情况-全部正常"
#         sites_info = [title]

#     base_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=168fb726-b09c-4061-9829-f1fbc5cc6ae5'
#     json_data = {
#         'msgtype': 'markdown',
#         'markdown': {
#             'content': "\n".join(sites_info),
#         }
#     }

#     if day_task:
#         response = requests.post(base_url, json=json_data)
#         return response.json()
#     else:
#         if bad_sites:
#             response = requests.post(base_url, json=json_data)
#             return response.json()
#         else:
#             return ''


# # 每小时执行一次
# @periodic_task(run_every=3600)
# def verification_website():
#     sites = Site.objects.filter(is_ignore=False)

#     good_history, bad_sites = tools.verificate_site_list(sites, daily=False)
#     response = send_msg_to_wx(bad_sites)

#     return response


# # 每天发送一封邮件
# @periodic_task(run_every=crontab(minute=0, hour=10))
# def send_daily_situation():
#     sites = Site.objects.filter(is_ignore=False)
#     good_history, bad_sites = tools.verificate_site_list(sites, daily=True)

#     html = render_to_string("app/email.html", {"site_history": data})
#     response = send_msg_to_wx(bad_sites, day_task=True)

#     return response



@periodic_task(run_every=60)
def backup_db_periodic_task():
    site = Site.objects.filter(name="航空订票").first()
    path = site.project_path
    os.chdir(path)

    print(os.system("python3 manage.py dumpdata > data.json"))
