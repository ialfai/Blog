from django.shortcuts import render
from .models import Board, Article


# Create your views here.
from django.views import View


class MainPageView(View):
    def get(self, request):
        return render(request, 'main_page.html')
    #trzeba podpiąć strony pod linki: top 10 artykułów


class BoardsPage(View):
    def get(self, request):
        boards = Board.objects.filter(user_id=3)
        #tu musi pobierać user_id z cookies po zalogowaniu
        return render(request, 'boards_page.html', {'boards': boards})
    #trzeba podpiąć strony wnętrza boardów pod linki


class BoardView(View):
    def get(self, request, board_id):
        board = Board.objects.get(id=board_id)
        articles = Article.objects.filter(board=board)
        return render(request, 'board_page.html', {'articles': articles,
                                                   'board': board})
    #tu trzeba podpiąć odpowiednie linki pod artykuły


class ArticlePage(View):
    def get(self, request, article_id):
        pass








