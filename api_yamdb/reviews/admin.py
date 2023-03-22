from django.contrib import admin

from .models import Title, Category, Genre, Review, Comment


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
