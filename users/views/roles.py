#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import HttpResponse,redirect
from django.views.generic import ListView,CreateView,View,UpdateView
from users.models import AuthRole,UserProfile,AuthMenu
from users.forms.roles import RolesCreateForm,RolesUpdateForm
from django.urls import reverse_lazy
from django.http import JsonResponse

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
            "parent_id": key["parent_id"],
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

class RolesListViews(ListView):
    template_name = "users/roles_list.html"
    model = AuthRole

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': "用户管理",
            'action':"角色列表",
        })
        return context

class RolesCreateViews(CreateView):
    template_name = "users/roles_create.html"
    model = AuthRole
    form_class = RolesCreateForm

    def get_context_data(self, **kwargs):
        nodes = AuthMenu.objects.all()
        context = super().get_context_data(**kwargs)
        menu_dic = menu_recursive()
        context.update({
            'app': "用户管理",
            'action':"角色创建",
            "menu_dic": menu_dic,
            "nodes": nodes,
        })
        return context

    def post(self,request, *args, **kwargs):
        name = request.POST.get("name")
        menu_list = request.POST.getlist("menu_list")
        obj = AuthRole.objects.filter(name=name)
        if obj:
            pass
        else:
            user_roles = AuthRole.objects.create(name=name)
            user_roles.menu.add(*menu_list)
        return redirect("users:roles-list")

class RolesDeleteViews(View):
    model = UserProfile

    def post(self,request):
        id = request.POST.get("uid")
        AuthRole.objects.filter(id=id).delete()
        data = {"code": 0, "info": "删除成功"}
        return JsonResponse(data)

class RolesUpdateViews(UpdateView):
    template_name = "users/roles_edit.html"
    model = AuthRole
    form_class = RolesUpdateForm
    success_url = reverse_lazy('users:roles-list')

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        role_obj = AuthRole.objects.filter(id=pk).first()
        nodes = AuthMenu.objects.all()
        menu_dic = menu_recursive()
        menu_obj = role_obj.menu.values_list("id")
        menu = []
        for key in menu_obj:
            menu.append(int(key[0]))
        context = super().get_context_data(**kwargs)
        context.update({
            'app': "用户管理",
            'action':"角色更新",
            'nodes':nodes,
            'menu':menu,
            'menu_dic': menu_dic,
            'pk':pk,
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        name = request.POST.get("name")
        menu_list = request.POST.getlist("menu_list")
        menu_all = AuthMenu.objects.filter(id__in=menu_list)
        user_roles = AuthRole.objects.get(name=name)
        user_roles.menu.clear()
        user_roles.menu.add(*menu_all)
        return redirect("users:roles-list")

