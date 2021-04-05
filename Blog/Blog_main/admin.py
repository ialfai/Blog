from django.contrib import admin
from Blog_main.models import User, Interests, Article, Board, UsersInterest, Authors

# Register your models here.

admin.site.register(Interests)
admin.site.register(Article)
admin.site.register(Board)
admin.site.register(UsersInterest)
admin.site.register(Authors)




