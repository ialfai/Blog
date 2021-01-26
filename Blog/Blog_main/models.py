from django.db import models
from django.db.models import CASCADE
# Create your models here.


class Interests(models.Model):
    name = models.CharField(max_length=288)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=300)
    creation_date = models.DateField(auto_created=True)
    active_status = models.BooleanField(default=True)
    interests = models.ManyToManyField(Interests)
    writer = models.BooleanField(default=False)


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=CASCADE)


STATUS = (
    ('in the process', 1),
    ('proofreading', 2),
    ('published', 3)
)


class Article(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    requests_number = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=CASCADE)
    status = models.IntegerField(choices=STATUS)
    publishing_date = models.DateField()
    content = models.TextField(null=True)


COLORS = (
    ('', 1),
    ('', 2),
    ('', 3)
)


class Board(models.Model):
    article = models.ManyToManyField(Article)
    name = models.CharField(max_length=255)
    background_color = models.IntegerField()
    public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=CASCADE)


