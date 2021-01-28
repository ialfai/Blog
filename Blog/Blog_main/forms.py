import django.forms as forms
from django.contrib.auth.models import User
from .models import Board, Article, Interests, STATUS
from django.contrib.admin.widgets import FilteredSelectMultiple


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


class AddArticle(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    author = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    publishing_date = forms.DateField(label='Publishing Date', widget=forms.SelectDateWidget)
    content = forms.CharField(widget=forms.Textarea)
    interests = forms.ModelMultipleChoiceField(queryset=Interests.objects.all(),
                                               widget=forms.CheckboxSelectMultiple)
    status = forms.ChoiceField(choices=STATUS)
