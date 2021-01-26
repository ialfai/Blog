from django.contrib.auth import authenticate, login, logout
from django.forms import forms
import django.forms as forms
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from Blog_main.models import User


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['interests', 'active_status', 'creation_date', 'writer']

