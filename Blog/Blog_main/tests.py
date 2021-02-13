import pytest
from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from conftest import unauthorized_user, client, test_article, test_board, authorized_user
from Blog_main.models import Board, Interests
# Create your tests here.


@pytest.mark.django_db
def test_unauthorized_user(client, unauthorized_user):
    client.force_login(unauthorized_user)
    response = client.get('/new_article/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_request_article(client, unauthorized_user, test_article):
    client.force_login(unauthorized_user)
    response = client.post(f'/article/{test_article.id}', {'RequestArticle': ''})
    test_article.refresh_from_db()
    assert test_article.requests_number == 1


@pytest.mark.django_db
def test_login(client):
    response = client.post('/new_board')
    assert response.status_code == 301


@pytest.mark.django_db
def test_add_article_to_board(client, test_article, test_board, unauthorized_user):
    client.force_login(unauthorized_user)
    response = client.post(f'/article/{test_article.id}', {'AddToBoard': '',
                                                          'board': test_board.id
                                                          })
    assert test_article in test_board.article.all()


@pytest.mark.django_db
def test_register(client):
    response = client.post('/register/', {'first_name': 'lola',
                                          'last_name': 'bzik',
                                          'username': 'malinka',
                                          'password': 'haha',
                                          'email': 'hgjhg@hjkhjk.com'})
    print(response.content)
    assert response.status_code == 302
    assert User.objects.get(username='malinka')


@pytest.mark.django_db
def test_add_new_board(client, unauthorized_user):
    client.force_login(unauthorized_user)
    response = client.post('/new_board/', {'name': 'podróże',
                                           'picture': ''})

    assert Board.objects.filter(name='podróże', user=unauthorized_user)

#
# @pytest.mark.django_db
# def test_add_interests(client, authorized_user):
#     client.force_login(authorized_user)
#     response = client.post('/new_interest/', {'interest': 'gotowanie'})
#     assert Interests.objects.filter(user=authorized_user).name == 'gotowanie'


@pytest.mark.django_db
def test_do_the_quiz(client, unauthorized_user, test_interests):
    client.force_login(unauthorized_user)
    response = client.post('/quiz/', {'interest': test_interests.id})
    assert test_interests in Interests.objects.filter(user=unauthorized_user)




