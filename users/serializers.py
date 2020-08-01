#!/usr/bin/env python
#-*- coding:utf-8 -*-
from .models import UserProfile
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = [ 'username', 'email']

