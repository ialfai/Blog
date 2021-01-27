import django.forms as forms
from django.contrib.auth.models import User
from .models import Board


class Login(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class Register(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class NewBoard(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ['article', 'background_color', 'public', 'user']

