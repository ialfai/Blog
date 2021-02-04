import pytest
from django.contrib.auth.models import User
from django.test import Client
from Blog_main.models import Article, Board


@pytest.fixture
def unauthorized_user():
    unauthorized_user = User.objects.create_user(username='Ania', password='haha')
    return unauthorized_user


@pytest.fixture
def another_user():
    another_user = User.objects.create_user(username='Zdzisława', password='haha')
    return another_user


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def test_user():
    pass


@pytest.fixture
def test_article():
    article = Article.objects.create(name='test_article',
                                     description='test_description',
                                     author=User.objects.create_user('Ula'),
                                     status=3,
                                     publishing_date='2020-01-01',
                                     picture=None)
    return article


@pytest.fixture
def test_board(unauthorized_user):
    test_boards = Board.objects.create(name='test_name',
                                       user=unauthorized_user)
    return test_boards


