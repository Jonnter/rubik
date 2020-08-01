#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from users.models import UserProfile,AuthRole
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=100,
        widget=forms.TextInput(attrs={"class":"form-control" ,"placeholder":"请输入您的用户名" ,"required":"","type":"username","name":"username","id":"username" }),
        required=True,
        error_messages={'required':u'用户名不能为空'}
    )
    password = forms.CharField(
        label='password',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入密码", "required": "","type":"password","name":"password","id":"password"}),
        max_length=128,
        strip=False,
        required=True,
        error_messages={'required': u'密码不能为空'}

    )
    # captcha = CaptchaField(
    #     label='验证码',
    #     required=True,
    #     widget=forms.TextInput(attrs={"class": "form-control","placeholder":"验证码"}),
    #     error_messages={
    #         'required': '验证码不能为空'
    #     }
    # )

    def clean(self):
        username = self.cleaned_data.get("username")
        pwd = self.cleaned_data.get("password")
        user = auth.authenticate(username=username, password=pwd)
        if user is None:
            raise forms.ValidationError(message=u'请输入一个正确的用户名和密码.')
        elif not user.is_active:
            raise forms.ValidationError(message=u'此账号已被禁用')
        else:
            return self.cleaned_data


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs = {"name": "password", "class": "form-control", "autocomplete": "new-password",
                 "placeholder": "请输入数字，大小写字母，特殊字符组合使用！（6-16位）"}),
        max_length=128, strip=False, required=False,

    )

    class Meta:
        model = UserProfile
        fields = ["username","email", "mobile", "roles", "is_superuser", "comment","name" ]
        widgets = {
            'name': forms.TextInput(
                attrs={"class": "form-control", "name": "name", "required": "required","placeholder":"输入真实姓名"}
            ),
            'username':forms.TextInput(
                attrs={"class":"form-control","name":"uername","required":"required","placeholder":"输入登录名"}
            ),

            "email":forms.EmailInput(
                attrs={"name":"email","required": "required","class" :"form-control" ,"placeholder":"输入email"}
            ),
            "mobile":forms.TextInput(
                attrs={"name":"mobile","class":"form-control","required":"required","maxlength":"11","placeholder":"输入手机号"}
            ),
            "roles": forms.Select(
                attrs={"class":"form-control","required":"required","name":"role_id"}
            ),
            "comment":forms.Textarea(
                attrs={"cols":"40","rows":"5","maxlength":"200","class":"form-control","placeholder":"简介","name":"comment"}
            ),
        }

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        user = super().save(commit=commit)
        if password:
            user.reset_password(password)
        return user

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["username","email", "mobile", "roles", "is_superuser", "comment","name" ]
        widgets = {
            'name': forms.TextInput(
                attrs={"class": "form-control", "name": "nickname", "id": "nickname"}
            ),
            'username':forms.TextInput(
                attrs={"class":"form-control","name":"uername","id": "username"}
            ),

            "email":forms.EmailInput(
                attrs={"class" :"form-control","name":"email","placeholder":"请输入正确的邮箱"}
            ),
            "mobile":forms.TextInput(
                attrs={"class":"form-control","name":"mobile","id":"mobile","placeholder":"请输入正确的手机号"}
            ),
            "roles": forms.Select(
                attrs={"class":"form-control","name":"role_id","id":"role_id"}
            ),
            "comment":forms.Textarea(
                attrs={"class":"form-control","placeholder":"简介","name":"comment","id":"remark","rows":"3"}
            ),
            # 'is_superuser': forms.MultipleChoiceField(
            #     choices=((True, _("Administrator")), (False, _("User"))),
            #     widget={'class': 'form-control switch-success switch-solid'}
            # )
        }


class UserChangePassForm(forms.Form):

    oldpwd = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"name": "oldpwd", "class": "form-control", "id":"old-password","autocomplete": "old-password","placeholder":"输入账号的原登录密码", "required": "required"}),
        max_length=128, strip=False, required=False
    )
    newpwd = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"name": "newpwd", "class": "form-control", "id": "newpwd", "autocomplete": "new-password",
                   "placeholder": "输入新的密码", "required": "required"}),
        max_length=128, strip=False, required=False
    )
    confirmpwd = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"name": "confirmpwd", "class": "form-control", "id": "confirmpwd", "autocomplete": "confirm-password",
                   "placeholder": "确认新密码", "required": "required"}),
        max_length=128, strip=False, required=False
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_oldpwd(self):
        old_password = self.cleaned_data.get("oldpwd")
        if not self.user.check_password(old_password):
            print("not")
            raise forms.ValidationError(message=u'原密码错误')
        return old_password

    def clean_confirmpwd(self):
        password1 = self.cleaned_data.get('newpwd')
        password2 = self.cleaned_data.get('confirmpwd')
        if len(password1) < 6:
            raise forms.ValidationError(message=u'新密码必须大于6位')

        if password1 and password2:
            print("ok")
            if password1 != password2:
                raise forms.ValidationError(message=u'两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data.get('newpwd'))
        if commit:
            self.user.save()
        return self.user


