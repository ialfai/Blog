from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.models import User

from .models import Board, Article
from .forms import Login, Register

# Create your views here.
from django.views import View


class MainPageView(View):
    def get(self, request):
        return render(request, 'main_page.html')
    #trzeba podpiąć strony pod linki: top 10 artykułów


class BoardsPage(View):
    def get(self, request):
        boards = Board.objects.filter(user_id=4)
        #tu musi pobierać user_id z cookies po zalogowaniu
        return render(request, 'boards_page.html', {'boards': boards})


class BoardView(View):
    def get(self, request, board_id):
        board = Board.objects.get(id=board_id)
        articles = Article.objects.filter(board=board)
        return render(request, 'board_page.html', {'articles': articles,
                                                   'board': board})


class ArticlePage(View):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        author = article.author
        return render(request, 'article_page.html', {'article': article,
                                                     'author': author})


class LogInPage(View):

    def get(self, request):
        form = Login()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form,
                                                      'info': "Wrong login data"})
        return render(request, 'login.html', {'form': form,
                                              'info': "Wrong login data 1"})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class Registration(View):

    def get(self, request):
        form = Register()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        pass






