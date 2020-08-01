#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf import settings
from users.models import AuthRole

def init_permission(request,user):
    menu_all = AuthRole.objects.filter(name=user.roles,menu__is_state=1).values('menu__url','menu__name','menu__parent_id','menu__icon',"menu__id","menu__only","menu__wight","menu__type").distinct()
    menu_dic = {}
    menu_list = []
    for key in menu_all:
        menu_id = key["menu__id"]
        menu_pid = key["menu__parent_id"]
        menu_list.append(key["menu__url"])
        menu_type = key["menu__type"]
        if menu_type == 1:
            if menu_pid not in  menu_dic:
                menu_dic[menu_id] = {
                    "name": key["menu__name"],
                    "only": key["menu__only"],
                    "icon":key["menu__icon"],
                    "wight":key["menu__wight"],
                    "type":menu_type,
                    "children":[],
                }
            else:
                menu_dic[menu_pid]["children"].append({"name": key["menu__name"], "url": key["menu__url"],"parent_id":key["menu__parent_id"]})
    request.session[settings.MENU_SESSION_KEY] = menu_dic
    request.session[settings.PERMISSION_SESSION_KEY] = menu_list
    request.session['is_login'] = True