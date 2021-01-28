from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.models import User

from .models import Board, Article
from .forms import Login, Register, NewBoard, AddArticle

# Create your views here.
from django.views import View


class MainPageView(View):
    def get(self, request):
        return render(request, 'main_page.html')
    #trzeba podpiąć strony pod linki: top 10 artykułów


class BoardsPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            boards = Board.objects.filter(user_id=user_id)
            return render(request, 'boards_page.html', {'boards': boards})
        else:
            pass


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
        user = request.user
        boards = Board.objects.filter(user=user)
        print(boards)
        return render(request, 'article_page.html', {'article': article,
                                                     'author': author,
                                                     'boards': boards})

    def post(self, request, article_id):
        if 'AddToBoard' in request.POST:
            boards = request.POST.get('board')
            article = Article.objects.get(id=article_id)
            author = article.author
            user = request.user
            boards_for_checkbox = Board.objects.filter(user=user)
            b = Board.objects.get(id=boards)
            b.article.add(article)
            b.save()
            return render(request, 'article_page.html', {'article': article,
                                                         'author': author,
                                                         'boards': boards_for_checkbox,
                                                         'info': 'Article has been added to the chosen board'})
        if 'RequestArticle' in request.POST:
            article = Article.objects.get(id=article_id)
            article.requests_number += 1
            article.save()
            user = request.user
            boards = Board.objects.filter(user=user)
            author = article.author
            return render(request, 'article_page.html', {'article': article,
                                                         'author': author,
                                                         'boards': boards})


class LogInPage(View):

    def get(self, request):
        form = Login()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
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
        form = Register(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'],
                                     email=form.cleaned_data['email'],
                                     first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'])
            return redirect('/login/')
        else:
            return render(request, 'login.html', {'form': form,
                                                  'info': 'The data is incorrect'})


class AddingNewBoard(View):
    def get(self, request):
        form = NewBoard()
        return render(request, 'new_board.html', {'form': form})

    def post(self, request):
        form = NewBoard(request.POST)
        if form.is_valid():
            user_id = request.user.id
            new_board = Board.objects.create(name=form.cleaned_data['name'],
                                             user_id=user_id)
            return redirect('/boards/')
        else:
            return render(request, 'new_board.html', {'form': form,
                                                      'info': 'Incorect date'})


class AddNewArticle(View):
    def get(self, request):
        form = AddArticle()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AddArticle(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            author_ins = User.objects.get(username=author[0])
            interests = form.cleaned_data['interests']
            new_article = Article.objects.create(name=form.cleaned_data['name'],
                                                 description=form.cleaned_data['description'],
                                                 author=author_ins,
                                                 publishing_date=form.cleaned_data['publishing_date'],
                                                 status=form.cleaned_data['status'],
                                                 content=form.cleaned_data['content'])
            new_article.interests.set(interests)
            return redirect('/all_articles/')
        else:
            return render(request, 'login.html', {'form': form,
                                                  'info': 'There are errors in the form'})


class AllArticles(View):
    def get(self, request):
        articles = Article.objects.all()
        return render(request, 'all_articles.html', {'articles': articles})