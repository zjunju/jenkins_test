from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.core import paginator
from django.template.loader import render_to_string
from django.conf import settings

from .forms import SiteForm
from .models import Site, SiteHistory

from utils.jsonResponse import jsonFailed, jsonSuccess
from utils import tools

import os
import requests
import json
from fabric import Connection
import time
from html.parser import HTMLParser

from invoke.exceptions import UnexpectedExit


@require_GET
def index(request):
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    sites = Site.objects.all()

    history_list = SiteHistory.objects.all()
    # 每页显示站点检测历史记录数量为站点总数, 最小为1
    each_page_number = max(sites.count(), 1)
    pagination = paginator.Paginator(history_list, each_page_number)

    try:
        page_obj = pagination.page(page)
    except paginator.EmptyPage:
        page_obj = pagination.page(1)

    context = {}
    context['sites'] = sites
    context['history_list'] = history_list
    context['page_obj'] = page_obj
    return render(request, "app/index.html", context)


@require_POST
def add_site(request):
    form = SiteForm(request.POST)
    if form.is_valid():
        site_id = request.POST.get("site_id")
        name = form.cleaned_data.get('name', None)
        href = form.cleaned_data.get('href', None)
        coding = form.cleaned_data.get('coding', None)
        restart = form.cleaned_data.get('restart', None)
        deploy = form.cleaned_data.get('deploy', None)
        update_cert = form.cleaned_data.get('update_cert', None)
        copy = form.cleaned_data.get('copy', None)

        need_verification = True if request.POST.get("custom-switch-checkbox") == 'on' else False
        overseas = True if request.POST.get("overseas-switch-checkbox") == 'on' else False

        if site_id:
            site = Site.objects.filter(id=int(site_id)).first()
            action = "change"
            site_tr_html = None
            if site:
                site.name = name
                site.href = href
                site.coding = coding
                site.need_verification = need_verification
                site.restart = restart
                site.deploy = deploy
                site.update_cert = update_cert
                site.copy = copy
                site.overseas = overseas
                site.save()

                msg = "修改成功"
                msg_type = "success"
                site_tr_html = tools.get_html('app/site-tr.html', {'site': site})
            else:
                msg = "修改失败，没有找到该站点，也许站点已经被删除"
                msg_type = "danger"
        else:
            site = Site.objects.create(name=name, href=href, coding=coding,
                                    need_verification=need_verification, copy=copy,
                                    deploy=deploy, restart=restart, 
                                    update_cert=update_cert, overseas=overseas)
            msg = "添加成功"
            msg_type = "success"
            action = "create"
            site_tr_html = tools.get_html('app/site-tr.html', {'site': site})

        msg_html = tools.get_html('app/msg.html', {'msg': msg, 'msg_type': msg_type})
        return jsonSuccess(msg="添加成功", data={"site_tr_html": site_tr_html,\
                            'msg_html': msg_html, 'action': action, 'site_id': site.id})

    else:
        errors = form.get_errors(data_type='list')
        msg = errors[0].get("message", None) if errors else '添加失败'
        msg_html = tools.get_html('app/msg.html', {'msg': msg, 'msg_type': 'danger'})
        return jsonFailed(code = 401, msg = msg, data={'msg_html': msg_html})


@require_POST
def delete_site(request):
    site_id = request.POST.get("site_id", None)
    if site_id:
        site = Site.objects.filter(pk=int(site_id)).first()
        if site:
            site.delete()
            msg = '删除成功'
            html = tools.get_html(html_path="app/msg.html",data={'msg': msg, 'msg_type': 'success'})
            return jsonSuccess(msg=msg, data={"html": html})

    return jsonFailed(code=401,msg="没有找到该站点！该站点可能已经被删除")


def verification(request):
    
    site_pk_list = request.POST.getlist('site-pk-checkbox')
    sites = []
    if request.POST.get("verificate-all"):
        sites = Site.objects.all()

    sites = []
    if site_pk_list:
        for each in site_pk_list:
            site = Site.objects.filter(id=each).first()
            if site:
                sites.append(site)
    if not sites:
        sites = Site.objects.all()

    good, bad = tools.verificate_site_list(sites)
    good.extend(bad)
    SiteHistory.objects.bulk_create(good)
    
    return redirect('/')


def send_email(request):
    sites = Site.objects.all()
    result = tools.verificate_site_list(sites)

    html = render_to_string("app/email.html",{"site_history": result})
    return HttpResponse(html)


@require_POST
def change_ignore(request):
    site_pk = request.POST.get('site_pk', 0)
    checked = request.POST.get('checked', None)
    site = Site.objects.filter(id=site_pk).first()

    site.is_ignore = True if checked == 'true' else False
    site.save()
    return jsonSuccess()


@require_POST
def run_script(request):
    site_pk = request.POST.get("site_id", 0)
    action = request.POST.get("action", "")

    # 什么也不做
    if not action:
        return jsonFailed(5, "没有要执行的文件")

    site = Site.objects.filter(pk=site_pk).first()
    if not site:
        return jsonFailed(1, msg="没有找到该站点！该站点可能已经被删除")

    action_dict = {'restart': site.restart, 'deploy': site.deploy, 'update_cert': site.update_cert}

    file_name = action_dict.get(action, "")

    if not file_name:
        return jsonFailed(1, msg="该站点未设置脚本文件")

    # 连接服务器
    user = 'root'
    host = settings.SERVER_HOST
    key_filename = settings.KEY_FILENAME_PATH

    result = Connection(host, user=user, connect_kwargs={"key_filename": key_filename})

    # script_file = os.path.join(settings.SCRIPT_PATH, file_name)
    
    try:
        # 要执行的命令
        with result.cd(script_file):
            result = result.run("python3 %s"%file_name)
            msg = result.stdout

        return jsonSuccess(msg="返回结果："+msg)

        # print('return_code', pwd.return_code)
        # print('stdout', pwd.stdout)
    except UnexpectedExit as e:
        return jsonFailed(2, msg="执行命令错误")

