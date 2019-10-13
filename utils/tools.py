from django.template.loader import render_to_string
from django.conf import settings

from app.models import SiteHistory, Site

from datetime import datetime
import requests
# from urllib3.contrib import pyopenssl as reqs

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import ssl
import socket
import time
from functools import partial

from multiprocessing.dummy import Pool as ThreadPool


headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }


def get_html(html_path, data={}):
    if isinstance(data, dict):
        return render_to_string(html_path, data)
    else:
        raise TypeError("请传入一个字典类型的数据")


def set_data_list(data:dict):
    new_data = []
    for key, values in data.items():
        for value in values:
            new_data.append(value)

    return new_data


def set_data_dict(data:dict):
    new_data = {}
    for key, values in data.items():
        new_data[key] = []
        for value in values:
            new_data[key].append(value)

    return new_data


class MixinForm(object):
    def get_errors(self, data_type='dict'):
        if getattr(self, "errors"):
            if data_type == 'list':
                return set_data_list(self.errors.get_json_data())
            else:
                return set_data_dict(self.errors.get_json_data())
        else:
            if data_type == 'list':
                return []
            else:
                return {}


def normal_vertificate(site, site_type=None):
    """ 网站状况监测  状态码 响应时间 """
    schema = 'https://' if site.need_verification else 'http://'
    url = schema + site.href

    try:
        timeout = 10
        # 如果是海外服务器
        if site.overseas:
            timeout = settings.OVERSEAS_TIMEOUT
        response = requests.get(url=url, headers=headers, timeout=timeout)
        ping_time = round(response.elapsed.total_seconds() * 1000, 0)
        if response.status_code != 200:
            site_type = '3'
            result = "网站访问异常"
            status_code = response.status_code
        else:
            if ping_time > timeout * 1000:
                site_type = '4'
                result = "连接超时"
                ping_time = None
                status_code = "连接超时"
            else:
                status_code = response.status_code
                result = "正常"
                site_type = site_type if site_type else '1'

    except (requests.exceptions.ConnectTimeout,  requests.exceptions.ReadTimeout):
        ping_time = None
        site_type = '4'
        status_code = "连接超时"
        result = "连接超时"

    except Exception as e:
        ping_time = None
        site_type = '4'
        status_code = e.__str__()
        result = e.__str__()

    return ping_time, site_type, status_code, result


def certificate_vertificate(site):
    """ 
        证书状况检测 
        param: site Site object
        return: remain_days(int)  or None 
    """
    try:
        context = ssl.create_default_context()
        host = site.href.split('/')[0]
        conn = context.wrap_socket(socket.socket(socket.AF_INET),
                                    server_hostname=host)
        conn.connect((host, 443))
        cert = conn.getpeercert()
        end_time = datetime.strptime(cert.get('notAfter'), '%b %d %H:%M:%S %Y %Z')

    except Exception as e:
        return None
    
    current_time = datetime.now()
    remain_days = (end_time - current_time).days

    return remain_days


def vertificate_site(site, daily):
    site_type = None
    if daily and site.need_verification:
        # 获取站点证书剩余时间
        remain_days = certificate_vertificate(site)

        if remain_days is None:
            result = "网站访问异常"
            status_code = "网站访问异常"
            site_type = '4'
            certificate = None
            ping_time = None
            return SiteHistory(site=site, site_type=site_type,
                                ping_time=ping_time, result=result, \
                                certificate=certificate, status_code=status_code)

        if remain_days < 14:
            result = '证书即将过期'
            site_type = '2'
            certificate = remain_days
        elif remain_days <= 0:
            certificate = 0
            result = "证书已过期"
        else:
            certificate = remain_days
    else:
        certificate = None

    # 获取站点普通情况
    ping_time, site_type, status_code, result = normal_vertificate(
                                                            site, site_type)

    siteHistory = SiteHistory(site=site, site_type=site_type,
                            ping_time=ping_time, result=result,
                            certificate=certificate, status_code=status_code)

    return siteHistory


def verificate_bad_sites(siteHistoryList, daily=False, times=1):
    bad_sites = []

    for siteHistory in siteHistoryList:
        result = vertificate_site(siteHistory.site, daily)
        if result.site_type == '4':
            bad_sites.append(result)

    if bad_sites and times < 4:
        bad_sites = verificate_bad_sites(bad_sites, times=times+1)
    
    return bad_sites


def verificate_site_list(sites, daily=True):
    good_history = []
    bad_history = []
    time_out_sites = []

    pool = ThreadPool()

    vertificate_site_true = partial(vertificate_site, daily=daily)
    siteHistory_list = pool.map(vertificate_site_true, sites)

    for siteHistory in siteHistory_list:
        if siteHistory.site_type == '4':
            time_out_sites.append(siteHistory)
        elif siteHistory.site_type != '1':
            bad_history.append(siteHistory)
        else:
            good_history.append(siteHistory)

    if time_out_sites:
        time_out_sites = verificate_bad_sites(time_out_sites)

    bad_history.extend(time_out_sites)
    return good_history, bad_history


# 发送邮件
def post_email(title, context):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(context, 'html', 'utf-8')
    message['From'] = Header(settings.EMAIL_SENDER)   # 发送者
    message['To'] =  Header(str(";".join(settings.EMAIL_RECEIVERS)))        # 接收者
    message['Subject'] = Header(title)
    try:
        smtpObj = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        smtpObj.login(settings.EMAIL_USER, settings.EMAIL_PASS)
        smtpObj.sendmail(settings.EMAIL_SENDER, settings.EMAIL_RECEIVERS, message.as_string())
        smtpObj.quit()
        return 1
    except smtplib.SMTPException:
        return 0
    
