from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.models import User


from .models import Board, Article, UsersInterest, Interests
from .forms import Login, Register, NewBoard, AddArticle, \
    AddInterestsForm, AddInterestsForm, QuizForm

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
        if Board.objects.filter(article=article, user=user):
            return render(request, 'article_page.html', {'article': article,
                                                         'author': author,
                                                         'stop': 'stop'})
        elif boards:
            return render(request, 'article_page.html', {'article': article,
                                                         'author': author,
                                                         'boards': boards})
        else:
            return render(request, 'article_page.html', {'article': article,
                                                         'author': author,
                                                         'info': 'To save this article, create a board!'})

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
            return redirect(f'/article/{article.id}')


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


class AddNewArticle(PermissionRequiredMixin, View):
    permission_required = 'blog_main.set_article'

    def get(self, request):

        form = AddArticle()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AddArticle(request.POST)
        if form.is_valid():
            interests = form.cleaned_data['interests']
            new_article = Article.objects.create(name=form.cleaned_data['name'],
                                                 description=form.cleaned_data['description'],
                                                 author=form.cleaned_data['author'],
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


class AddInterests(PermissionRequiredMixin, FormView):
    permission_required = 'blog_main.set_article'
    template_name = 'login.html'
    form_class = AddInterestsForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class QuizView(View):

    def get(self, request):
        form = QuizForm()
        interests = Interests.objects.all()
        return render(request, 'quiz.html', {'form': form,
                                             'interests': interests})

    def post(self, request):
        form = QuizForm(request.POST)
        if form.is_valid():
            user = request.user
            interests = form.cleaned_data['interest']
            users_old_interests = Interests.objects.filter(user=user)
            for a in users_old_interests:
                old_interests = Interests.objects.get(name=a)
                old_interests.user.remove(user)
            for i in interests:
                new_interests = Interests.objects.get(name=i)
                new_interests.user.add(user)
            return redirect('/dedicated_articles/')
        else:
            return render(request, 'quiz.html', {'form': form,
                                                 'info': 'Something went wrong'})


class DedicatedArticles(View):

    def get(self, request):
        user = request.user
        user_interests = Interests.objects.filter(user=user)
        articles = Article.objects.filter(interests__in=user_interests)
        return render(request, 'dedicated_articles.html', {'articles': articles})


