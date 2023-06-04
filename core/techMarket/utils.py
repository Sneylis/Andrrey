from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class DataMixin:
    def get_user_context(self,**kwargs):
        context = kwargs

        user_ok =self.request.user.is_authenticated


