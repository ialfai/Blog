from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User
# Create your models here.


class Interests(models.Model):
    name = models.CharField(max_length=288)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name



STATUS = (
    ('in the process', 1),
    ('proofreading', 2),
    ('published', 3)
)


class Article(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    requests_number = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=CASCADE)
    status = models.IntegerField(choices=STATUS)
    publishing_date = models.DateField()
    content = models.TextField(null=True)
    interests = models.ManyToManyField(Interests)


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


