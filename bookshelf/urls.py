from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    
    path("", views.home, name="home"),
    # example: /bookshelf/1/book/
    path("<int:book_id>/book/", views.book, name="book"),
    # example: /bookshelf/1/author/
    path("<int:author_id>/author/", views.author, name="author"),
    # example: /bookshelf/1/user/
    path("<int:user_id>/user/", views.user, name="user"),
    # example: /bookshelf/1/add/
    path("<int:book_id>/add/", views.add_userbook, name="add_userbook"),
]