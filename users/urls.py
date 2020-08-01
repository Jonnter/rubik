"""rubik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import login,users,menu,roles
from rest_framework import routers
from .api import UserViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register(r'api', UserViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', login.LoginViews.as_view(), name='login'),
    path('logout/', login.LogoutViews.as_view(), name='logout'),
    # # users
    path('users/', users.UsersListViews.as_view(), name='users-list'),
    path('add/', users.UsersCreateViews.as_view(), name='users-create'),
    path('del/', users.UsersDeleteViews.as_view(), name='users-delete'),
    path('<uuid:pk>/', users.UsersDetailView.as_view(), name='users-detail'),
    path('edit/<uuid:pk>/', users.UsersUpdateView.as_view(), name='users-edit'),
    path('edit/pwd/<uuid:pk>/', users.UsersEditPwdView.as_view(), name='users-edit-pwd'),
    path('edit/upload/', users.UsersUploadFileView.as_view(), name='users-edit-upload'),
    # # menu
    path('menu/', menu.MenuListViews.as_view(), name='menu-list'),
    path('menu/add/', menu.MenuListViews.as_view(), name='menu-create'),
    path('menu/del/', menu.MenuDeleteViews.as_view(), name='menu-delete'),
    path('menu/edit/<int:pk>/', menu.MenuUpdateViews.as_view(), name='menu-edit'),
    # # roles
    path('roles/', roles.RolesListViews.as_view(), name='roles-list'),
    path('roles/add/', roles.RolesCreateViews.as_view(), name='roles-create'),
    path('roles/del/', roles.RolesDeleteViews.as_view(), name='roles-delete'),
    path('roles/edit/<int:pk>/', roles.RolesUpdateViews.as_view(), name='roles-edit'),
]

urlpatterns += router.urls