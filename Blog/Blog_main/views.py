from django.shortcuts import render
from django.views.generic import FormView

from .models import Board, Article, Author
from .forms import LoginModelForm

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


class LogInPage(FormView):
    template_name = 'login.html'
    form_class = LoginModelForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)





