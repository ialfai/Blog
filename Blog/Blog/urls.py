"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Blog_main.views import MainPageView, BoardsPage, BoardView, \
    ArticlePage, LogInPage, Logout, Registration, AddingNewBoard,\
    AddNewArticle, AllArticles, AddInterests, QuizView, \
    DedicatedArticles, Extension, DeleteArticle, DeleteBoard, Top10
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view()),
    path('boards/', BoardsPage.as_view(), name='my_boards'),
    path('board/<int:board_id>', BoardView.as_view()),
    path('article/<int:article_id>', ArticlePage.as_view()),
    path('login/', LogInPage.as_view()),
    path('logout/', Logout.as_view()),
    path('register/', Registration.as_view()),
    path('new_board/', AddingNewBoard.as_view()),
    path('new_article/', AddNewArticle.as_view()),
    path('all_articles/', AllArticles.as_view()),
    path('new_interest/', AddInterests.as_view()),
    path('quiz/', QuizView.as_view()),
    path('dedicated_articles/', DedicatedArticles.as_view()),
    path('hints/', Extension.as_view()),
    path('delete_article/<int:article_id>/<int:board_id>', DeleteArticle.as_view()),
    path('delete_board/<int:board_id>', DeleteBoard.as_view()),
    path('top10/', Top10.as_view()),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

