#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from users.models import AuthMenu,AuthRole
# from mptt import forms as mf

class RolesCreateForm(forms.ModelForm):

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
        widgets = {
            'name':forms.TextInput(
                attrs={"class":"form-control title","name":"name","placeholder":"输入 标题"}
            ),
            "is_state":forms.RadioSelect(
                attrs={"type":"radio" ,"name":"is_state"}
            ),
        }


class RolesUpdateForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['menu'] = mf.TreeNodeChoiceField(
    #         queryset = AuthMenu.objects.all(),
    #         widget=forms.SelectMultiple(
    #             attrs={"class": "","type":"checkbox"}
    #             ),
    #     )
    #
    #     parent = mf.TreeNodeChoiceField(
    #         queryset = AuthRole.objects.none(),
    #     )

    class Meta:
        model = AuthMenu
        fields = ["name"]
        widgets = {
            'name': forms.TextInput(
                attrs={"class": "form-control title", "name": "name", "placeholder": "输入 标题"}
            ),
        }

    def clean(self):
        menu_list = self.cleaned_data.get("menu_list")
        for k,v in self.cleaned_data.items():
            print(k,v)
        return menu_list




