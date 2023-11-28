from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    # example: /bookshelf/
    path("", views.index, name="index"),
    # example: /bookshelf/1/book/
    path("<int:book_id>/book/", views.book, name="book"),
    # example: /bookshelf/1/author/
    path("<int:author_id>/author/", views.author, name="author"),
    # example: /bookshelf/1/user/
    path("<int:user_id>/user/", views.user, name="user"),
]