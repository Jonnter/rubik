#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 引入django
import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'rubik.settings'
import django
django.setup()

# 导入菜单/权限/角色
from users.models import AuthRole
from users.models import AuthMenu
from users.models import UserProfile

# Batch create menu
fa_users = AuthMenu.objects.create(name="用户管理",only="users",icon="mdi-account-multiple",wight=10)
# fa_dashboard = AuthMenu.objects.create(name="仪表盘",only="dashboard",icon="fa-dashboard",wight=1)

# 用户管理ID
user_manage = AuthMenu.objects.get(name="用户管理")
# dashboard = AuthMenu.objects.get(name="仪表盘")
# Batch create Permission
users_list = AuthMenu.objects.create(name="用户列表",url="/users/users/",parent_id=user_manage.id,only="users-list",wight=1)
user_id = AuthMenu.objects.get(name="用户列表")
users_add = AuthMenu.objects.create(name="用户添加",url="/users/add/",parent_id=user_id.id,only="users-add",wight=1,type=2)
users_edit = AuthMenu.objects.create(name="用户编辑",url="/users/edit/",parent_id=user_id.id,only="users-edit",wight=2,type=2)
users_del = AuthMenu.objects.create(name="用户删除",url="/users/del/",parent_id=user_id.id,only="users-del",wight=3,type=2)
#
users_role = AuthMenu.objects.create(name="角色列表",url="/users/roles/",parent_id=user_manage.id,only="roles-list",wight=2)
roles_id = AuthMenu.objects.get(name="角色列表")
role_add = AuthMenu.objects.create(name="角色添加",url="/users/roles/add/",parent_id=users_role.id,only="roles-add",wight=1,type=2)
role_edit = AuthMenu.objects.create(name="角色编辑",url="/users/roles/edit/",parent_id=users_role.id,only="roles-edit",wight=2,type=2)
role_del = AuthMenu.objects.create(name="角色删除",url="/users/roles/del/",parent_id=users_role.id,only="roles-del",wight=3,type=2)
#
users_menu = AuthMenu.objects.create(name="菜单列表",url="/users/menu/",parent_id=user_manage.id,only="menu-list",wight=3)
menu_id = AuthMenu.objects.get(name="菜单列表")
menu_add = AuthMenu.objects.create(name="菜单添加",url="/users/menu/add/",parent_id=users_menu.id,only="menu-add",wight=1,type=2)
menu_edit = AuthMenu.objects.create(name="菜单编辑",url="/users/menu/edit/",parent_id=users_menu.id,only="menu-edit",wight=2,type=2)
menu_del = AuthMenu.objects.create(name="菜单删除",url="/users/menu/del/",parent_id=users_menu.id,only="menu-del",wight=3,type=2)
##
# index = AuthMenu.objects.create(name="主页",url="/",parent_id=dashboard.id,only="index",wight=1)

# create user roles
menu_list = AuthMenu.objects.all()
user_roles = AuthRole.objects.create(name="管理员")
user_roles.menu.add(*menu_list)
#
# 导入用户模型
from users.models import UserProfile

# create superadmin
admin = UserProfile.objects.create_superuser(username="admin",password="123456")
users_roles_id = AuthRole.objects.get(name="管理员")
admin_obj = UserProfile.objects.filter(username="admin").update(roles=users_roles_id)
