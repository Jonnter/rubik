#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import template
from users.models import AuthRole,UserProfile,AuthMenu
from django.conf import settings
from collections import OrderedDict
from ..middleware import interceptor

register = template.Library()

@register.inclusion_tag("nav.html")
def menu(request):
    ordered_dict = OrderedDict()
    # menu_dic = request.session[settings.MENU_SESSION_KEY]
    # menu_all = interceptor.RabcMiddleWare()
    menu_dic,menu_list = interceptor.init_permission(request=request)
    ret = sorted(menu_dic,key = lambda x:menu_dic[x]['wight'])
    for i in ret:
        ordered_dict[i] = menu_dic[i]
    return {"menu_dic":ordered_dict.values(),'adminname':request.user.username}

@register.inclusion_tag('nav_li_profile.html')
def to_name(request):
    """user id 转位用户名称"""
    user_id = request.user.id
    try:
        user = UserProfile.objects.filter(id=user_id)
        if user:
            user = user[0]
            return user.name
    except:
        return '非法用户'

@register.filter(name="to_menu_pname")
def to_menu_pname(id):
    menu_name = AuthMenu.objects.filter(id=id)
    if menu_name:
        return menu_name.name
    else:
        return "Root"


