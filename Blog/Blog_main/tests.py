import pytest
from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from conftest import unauthorized_user, client, test_article
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
    response = client.post('/login', {'username': 'Ania', 'password': 'haha'})
    assert response.status_code == 301
    assert request.user.is_authenticated








