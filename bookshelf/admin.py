from django.contrib import admin
from .models import Book, Author, UserBook

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(UserBook)
