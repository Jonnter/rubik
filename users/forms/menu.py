#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from django.forms import widgets
from mptt import forms as mf
from django.utils.translation import gettext_lazy as _
from users.models import AuthMenu,AuthRole

class MenuCreateForm(forms.ModelForm):

    class Meta:
        menu_type = (
            (1, '菜单'),
            (2, '操作')
        )
        menu_state = (
            (0, '禁用'),
            (1, '启用')
        )
        model = AuthMenu
        fields = "__all__"
        # exclude = ["parent"]
        widgets = {
            'parent': forms.Select(
                attrs={"class": "form-control parent_id", "style": "width: 100%"}
            ),
            'name':forms.TextInput(
                attrs={"class":"form-control title","name":"name","placeholder":"输入 标题"}
            ),
            "icon":forms.TextInput(
                attrs={"class":"form-control icp icp-auto","name":"icon","value":"mdi-grease-pencil","id":"icon" ,"placeholder":"输入图标"}
            ),
            "wight":forms.TextInput(
                attrs={"id":"wight" ,"name":"wight", "value":"", "class":"form-control uri" ,"placeholder":"输入 权重"}
            ),
            "only":forms.TextInput(
                attrs={"id":"only" ,"name":"only" ,"value":"" ,"class":"form-control uri" ,"placeholder":"输入 标识"}
            ),
            "url":forms.TextInput(
                attrs={"class":"form-control uri","name":"url","id":"uri" , "value":"", "placeholder":"输入 路径"}
            ),
            "type":forms.RadioSelect(
                attrs={"type":"radio" ,"name":"type"}
            ),
            "is_state":forms.RadioSelect(
                attrs={"type":"radio" ,"name":"is_state"}
            ),
        }

class MenuUpdateForm(forms.ModelForm):

    class Meta:
        model = AuthMenu
        fields = "__all__"
        widgets = {
            'parent':forms.Select(
                attrs={"class": "form-control parent_id", "style": "width: 100%"}
            ),
            'name': forms.TextInput(
                attrs={"class": "form-control title", "name": "name", "placeholder": "输入 标题"}
            ),
            "icon": forms.TextInput(
                attrs={"class": "form-control icon iconpicker-element iconpicker-input", "name": "icon", "id": "icon",
                       "placeholder": "输入图标"}
            ),
            "wight": forms.TextInput(
                attrs={"id": "wight", "name": "wight", "value": "", "class": "form-control uri", "placeholder": "输入 权重"}
            ),
            "only": forms.TextInput(
                attrs={"id": "only", "name": "only", "value": "", "class": "form-control uri", "placeholder": "输入 标识"}
            ),
            "url": forms.TextInput(
                attrs={"class": "form-control uri", "name": "url", "id": "uri", "value": "", "placeholder": "输入 路径"}
            ),
            "type": forms.RadioSelect(
                attrs={"type": "radio", "name": "type"}
            ),
            "is_state": forms.RadioSelect(
                attrs={"type": "radio", "name": "is_state"}
            ),
        }




