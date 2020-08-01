#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib.auth import authenticate,login,logout
from django.shortcuts import reverse, redirect,HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from users.forms import users
from captcha.helpers import  captcha_image_url
from captcha.models import CaptchaStore
from users.models import UserProfile
from users.middleware import permission
from django.conf import settings
# from rubik.utils import create_logs

# Create your views here.


class LoginViews(FormView):
    template_name = "users/login.html"
    form_class = users.UserLoginForm

    def get(self,request, *args, **kwargs):
        return super().get( request,*args, **kwargs)

    def post(self,request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = self.request.POST.get("username")
            password = self.request.POST.get("password")
            # obj = UserProfile.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None :
                # permission.init_permission(request, obj)
                login(request,user)
                request.session['is_login'] = True
                # create_logs(request,msg="登录平台")
                return redirect("index")
        else:
            return super().form_invalid(form)

class LogoutViews(TemplateView):

    def get(self, request, *args, **kwargs):
        # create_logs(request, msg="退出平台")
        logout(request)
        return redirect(reverse("users:login"))
