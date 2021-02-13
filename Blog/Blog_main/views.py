from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.models import User


from .models import Board, Article, Interests
from .forms import Login, Register, NewBoard, AddArticle, \
    AddInterestsForm, AddInterestsForm, QuizForm

# Create your views here.
from django.views import View


class MainPageView(View):

    """This view is responsible for displaying the main page of the blog. It containst a navigation bar
     as well as login/registration option, access to all, best and chosen articles."""

    def get(self, request):
        return render(request, 'main_page.html')


class BoardsPage(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    """This view is responsible for displaying all boards that the user has created. It contains options of
    deleting an unwanted board and accessing any board"""

    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            boards = Board.objects.filter(user_id=user_id)
            return render(request, 'boards_page.html', {'boards': boards})
        else:
            return render(request, 'boards_page.html', {'info': 'You are not logged in. To create boards log in'})


class BoardView(View):

    """This view is responsible for displaying an inside of a given board with all the articles that have been
    saved inside of it. It allows user to also delete an unwanted article from the board."""

    def get(self, request, board_id):
        board = Board.objects.get(id=board_id)
        articles = Article.objects.filter(board=board)
        return render(request, 'board_page.html', {'articles': articles,
                                                   'board': board})


class ArticlePage(View):

    """This view is responsible for displaying an article with information regarding writer and publication date.
    There is a function for requesting the article and a function for adding it to a chosen board."""

    def get(self, request, article_id):
        article1 = Article.objects.get(id=article_id)
        author = article1.author
        user = request.user
        boards = Board.objects.filter(user=user)
        if boards:
            return render(request, 'article_page.html', {'article': article1,
                                                         'author': author,
                                                         'boards': boards})
        else:
            return render(request, 'article_page.html', {'article': article1,
                                                         'author': author,
                                                         'info': 'To save this article, create a board!'})

    def post(self, request, article_id):
        if 'AddToBoard' in request.POST:
            boards = request.POST.get('board')
            article1 = Article.objects.get(id=article_id)
            author = article1.author
            user = request.user
            boards_for_checkbox = Board.objects.filter(user=user)
            b = Board.objects.get(id=boards)
            b.article.add(article1)
            b.save()
            return render(request, 'article_page.html', {'article': article1,
                                                         'author': author,
                                                         'boards': boards_for_checkbox,
                                                         'info': 'Article has been added to the chosen board'})
        if 'RequestArticle' in request.POST:
            article1 = Article.objects.get(id=article_id)
            article1.requests_number += 1
            article1.save()
            author = article1.author
            user = request.user
            articles = Article.objects.all()
            boards_for_checkbox = Board.objects.filter(user=user)
            return render(request, 'article_page.html', {'article': article1,
                                                         'author': author,
                                                         'boards': boards_for_checkbox,
                                                         'articles': articles,
                                                         'info': 'Article has been added to the chosen board'})
            # return redirect(f'/article/{article.id}')


class LogInPage(View):

    """This view is responsible for displaying a login form. It allows registered user to login to the service"""

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

    """This view is responsible for logging the user out of the service"""

    def get(self, request):
        logout(request)
        return redirect('/')


class Registration(View):

    """This view is responsible for displaying a registration form. It allows new users to register to the service"""

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


class AddingNewBoard(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    """This view is responsible for displaying a form that allows users to create a new board. The user can choose
    a name and a theme picture for the board"""

    def get(self, request):
        form = NewBoard()
        return render(request, 'new_board.html', {'form': form})

    def post(self, request):
        form = NewBoard(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user.id
            new_board = Board.objects.create(name=form.cleaned_data['name'],
                                             user_id=user_id,
                                             picture=form.cleaned_data['picture'])
            return redirect('/boards/')
        else:
            return render(request, 'new_board.html', {'form': form,
                                                      'info': 'Incorect data'})


class AddNewArticle(PermissionRequiredMixin, View):

    """This is a restricted view, available only to moderators. This view is responsible for displaying
    a form to add a new article. Article has many features like: author data, publication date, article status,
    picture, requests number etc."""

    permission_required = 'blog_main.add_article'

    def get(self, request):

        form = AddArticle()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AddArticle(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            interests = form.cleaned_data['interests']
            new_article = Article.objects.create(name=form.cleaned_data['name'],
                                                 description=form.cleaned_data['description'],
                                                 author=form.cleaned_data['author'],
                                                 publishing_date=form.cleaned_data['publishing_date'],
                                                 status=form.cleaned_data['status'],
                                                 content=form.cleaned_data['content'],
                                                 picture=form.cleaned_data.get('picture'))
            new_article.interests.set(interests)
            return redirect('/all_articles/')
        else:
            return render(request, 'login.html', {'form': form,
                                                  'info': 'There are errors in the form'})


class AllArticles(View):

    """This view is responsible for displaying all articles that are in the database"""

    def get(self, request):
        articles = Article.objects.all()
        return render(request, 'all_articles.html', {'articles': articles})


class AddInterests(PermissionRequiredMixin, FormView):

    """This view is responsible for adding new fields of interest to the Interests table. This Interests table is used
    to label articles with interests. Based on this classification a user can choose what areas is he interested in.
    These interests are all displayed to the user in a quiz view"""

    permission_required = 'blog_main.set_interests'
    template_name = 'login.html'
    form_class = AddInterestsForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class QuizView(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    """This view is responsible for displaying a form that allows users to access articles based on their interests"""

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
            if users_old_interests:
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

    """This view is responsible for displaying to the user all articles that have been labeled with interests
    same as user has chosen in the quiz view"""

    def get(self, request):
        user = request.user
        user_interests = Interests.objects.filter(user=user)
        articles = Article.objects.filter(interests__in=user_interests)
        return render(request, 'dedicated_articles.html', {'articles': articles})


class Extension(View):

    """This view is responsible for creating a json file that will be used for the extension to list all available
    boards"""

    def get(self, request):
        id = request.GET.get('start')
        user = User.objects.get(id=id)
        boards = Board.objects.filter(user=user)
        boards_list = []
        for i in boards:
            boards_list.append(i.name)
        response = JsonResponse({'header':  'Access-Control-Allow-Origin: *',
                                 'boards_list': boards_list})
        return response


class DeleteArticle(View):

    """This view is responsible for remove an article from a given board"""

    def get(self, request, article_id, board_id):
        user = request.user
        article1 = Article.objects.get(id=article_id)
        board = Board.objects.get(id=board_id)
        board.article.remove(article1)
        return redirect('/boards')


class DeleteBoard(View):

    """This view is responsible for deleting a board"""

    def get(self, request, board_id):
        board = Board.objects.get(id=board_id)
        board.delete()
        return redirect('/boards')


class Top10(View):

    """This view is responsible for displaying 10 articles with biggest number of requests"""

    def get(self, request):
        articles = Article.objects.all().order_by('-requests_number')
        articles = articles[0:9]
        return render(request, 'top10.html', {'articles': articles})








