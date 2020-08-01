#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,View,UpdateView
from users.forms.menu import MenuUpdateForm,MenuCreateForm
from users.models import UserProfile,AuthMenu,AuthRole
from django.http import JsonResponse
import logging
import json
logger = logging.getLogger('rubik')

def menu_recursive():
    # 生成菜单字典
    menu_all = AuthMenu.objects.values('url','name','parent_id','icon',"id","only","wight","type").distinct()
    menu_dic = {}
    menu_list = []
    for key in menu_all:
        menu_id = key["id"]
        menu_pid = key["parent_id"]
        menu_type = key["type"]
        if menu_type == 1:

            if menu_pid not in  menu_dic:
                menu_dic[menu_id] = {
                    "id": key["id"],
                    "name": key["name"],
                    "only": key["only"],
                    "icon":key["icon"],
                    "wight":key["wight"],
                    "type":menu_type,
                    "children":[]
                }
            else:
                children_menu = get_child_menu(menu_id)
                if children_menu:
                    menu_dic[menu_pid]["children"].append({"id":key["id"],"name": key["name"], "url": key["url"],"parent_id":key["parent_id"],"children":children_menu})
                else:
                    menu_dic[menu_pid]["children"].append(
                        {"id": key["id"], "name": key["name"], "url": key["url"], "parent_id": key["parent_id"]})
    for key,values in menu_dic.items():
        menu_list.append(values)
    return menu_list

def get_child_menu(pid):
    # 获取所有子菜单
    child_list = []
    child_all = AuthMenu.objects.filter(parent_id=pid).values('url','name','parent_id','icon',"id","only","wight","type").distinct()
    for key in child_all:
        child_list.append({
            "id": key["id"],
            "name": key["name"],
            "only": key["only"],
            "wight": key["wight"],
            "url": key["url"]
        })
    return child_list

def get_object():
    menu_all = AuthMenu.objects.values('url','name','parent_id','icon',"id","only","wight","type").distinct()
    menu_dic = {}
    menu_list = []
    for key in menu_all:
        menu_id = key["id"]
        menu_pid = key["parent_id"]
        menu_type = key["type"]
        if menu_type == 1:
            if menu_pid not in  menu_dic:
                menu_dic[menu_id] = {
                    "id": key["id"],
                    "name": key["name"],
                    "children":[]
                }
            else:
                menu_dic[menu_pid]["children"].append({"id":key["id"],"name": key["name"]})
    for key,values in menu_dic.items():
        menu_list.append(values)
    return menu_dic

class MenuListViews(CreateView):
    template_name = "users/menu_list.html"
    model = AuthRole
    form_class = MenuCreateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        parent = request.POST.get("parent")
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect("users:menu-list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nodes = AuthMenu.objects.all()
        menu_dic = menu_recursive()
        context.update({
            'app': "用户管理",
            'nodes':nodes,
            'menu_dic':menu_dic,
            'action':"菜单列表",
        })
        return context

class MenuDeleteViews(View):
    model = AuthMenu

    def post(self,request):
        id = request.POST.get("id")
        AuthMenu.objects.filter(id=id).delete()
        data = {"status":0}
        return JsonResponse(data)

class MenuUpdateViews(UpdateView):
    template_name = "users/menu_edit.html"
    form_class = MenuUpdateForm
    model = AuthMenu
    success_url = reverse_lazy('users:menu-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': "用户管理",
            'action':"菜单更新",

        })
        return context