#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.shortcuts import redirect,HttpResponse
from django.views.generic import ListView,CreateView,View,DetailView,UpdateView,TemplateView,FormView
from users.forms.users import UserCreateForm,UserUpdateForm,UserChangePassForm
from users.models import UserProfile,AuthRole
from django.urls import reverse_lazy
from django.contrib.auth import logout
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from rubik.utils import create_logs
import json
import chardet
import os
from django.http import JsonResponse

class UsersListViews(ListView):
    template_name = "users/users_list.html"
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': "用户管理",
            'action':"用户列表",
        })
        return context

    def post(self,request):
        id = self.request.POST.get("id")
        password = self.request.POST.get("password")
        user = UserProfile.objects.get(id=id)
        user.reset_password(password)
        return redirect('users:users-list')

class UsersCreateViews(CreateView):
    template_name = "users/users_create.html"
    model = UserProfile
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': "用户管理",
            'action':"用户创建",
        })
        return context

    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            return redirect('users:users-list')
        else:
            return super().get(request, *args, **kwargs)

class UsersDeleteViews(View):
    model = UserProfile

    def post(self,request):
        id = request.POST.get("uid")
        username = UserProfile.objects.filter(id=id)
        # create_logs(request, msg="删除用户 %s" % username)  # 日志添加
        username.delete()
        data = {"code": 0, "info": "删除成功"}
        return JsonResponse(data)

class UsersDetailView(DetailView):
    model = UserProfile
    template_name = "users/users_detail.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = UserProfile.objects.filter(id=pk).first()
        context = {
            'app': "用户管理",
            'action': "用户详情",
            'object': detail,
            "uuid":pk,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class UsersUpdateView(UpdateView):
    form_class = UserCreateForm
    model = UserProfile
    template_name = "users/users_edit.html"
    success_url = reverse_lazy('users:users-list')

    def get_context_data(self, **kwargs):

        context = {
            'app': "用户管理",
            'action': "用户更新",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UsersEditPwdView(UpdateView):
    form_class = UserChangePassForm
    model = UserProfile
    template_name = "users/users_edit_pwd.html"
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):

        context = {
            'app': "用户管理",
            'action': "用户更新",
        }

        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        logout(self.request)
        return super().get_success_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

class UsersUploadFileView(View):
    model = UserProfile
    template_name = "users/users_edit_pwd.html"

    def post(self,request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        static = BASE_DIR + "/static/images/users"
        obj = request.FILES.get("file")
        print(obj)

        # with open("%s/%s"%(static,obj),"wb") as f:
        #     f.write(obj)
        # return HttpResponse('ok')