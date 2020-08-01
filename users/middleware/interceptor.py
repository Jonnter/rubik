#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import HttpResponseRedirect
from users.models import AuthRole,UserProfile
import re


def init_permission(request):
    user = UserProfile.objects.get(username=request.user)
    menu_all = AuthRole.objects.filter(name=user.roles, menu__is_state=1).values('menu__url', 'menu__name',
                                                                                      'menu__parent_id', 'menu__icon',
                                                                                      "menu__id", "menu__only",
                                                                                      "menu__wight",
                                                                                      "menu__type").distinct()
    menu_dic = {}
    menu_list = []
    for key in menu_all:
        menu_id = key["menu__id"]
        menu_pid = key["menu__parent_id"]
        menu_list.append(key["menu__url"])
        menu_type = key["menu__type"]
        if menu_type == 1:
            if menu_pid not in menu_dic:
                menu_dic[menu_id] = {
                    "name": key["menu__name"],
                    "only": key["menu__only"],
                    "icon": key["menu__icon"],
                    "wight": key["menu__wight"],
                    "type": menu_type,
                    "children": [],
                }
            else:
                menu_dic[menu_pid]["children"].append(
                    {"name": key["menu__name"], "url": key["menu__url"], "parent_id": key["menu__parent_id"]})
    return menu_dic,menu_list


class RabcMiddleWare(MiddlewareMixin):

    def process_request(self,request):
        # 用户登陆URL
        url = request.path_info
        # pattern = re.compile(r'/users/\w{8}(-\w{4}){3}-\w{12}')
        # m_pwd = re.compile(r'/users/edit/pwd/\w{8}(-\w{4}){3}-\w{12}')
        # 访问白名单匹配
        for key in settings.WHITE_LIST:
            if re.match(key,url):
                return None
        # 用户登陆状态
        is_login = request.session.get("is_login")
        # 用户登陆ID
        user_id = request.user.id
        # 修改个人信息URL匹配
        m_profile_url = r'/users/edit/%s/' %user_id
        # 修改个人密码URL匹配
        m_pwd = r'/users/edit/pwd/%s/' %user_id
        # 个人信息查看URL匹配
        pattern = r'/users/%s/' %user_id
        if is_login:
            if request.user.is_superuser:
                return None
            if url == m_pwd:
                return None
            if url == pattern:
                return None
            if url == m_profile_url:
                return None
            if request.user.roles == '管理员' and url == '/setting/':
                return None
            menu_dic,menu_list = init_permission(request)
            for key in menu_list:
                if str(key) in url:
                    return None
            print(request.user.is_superuser)
            return HttpResponseRedirect('/error_page')
        else:
            return HttpResponseRedirect("/")