from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    
    path("", views.home, name="home"),
    # home api response
    path("api/home/", views.home_api, name="home_api"),
    # example: /bookshelf/1/book/
    path("<int:book_id>/book/", views.book, name="book"),
    # example: /bookshelf/api/1/book/
    path("api/<int:book_id>/book/", views.book_api, name="book_api"),
    # example: /bookshelf/1/author/
    path("<int:author_id>/author/", views.author, name="author"),
    # example: /bookshelf/api/1/author/
    path("api/<int:author_id>/author/", views.author_api, name="author_api"),
    # example: /bookshelf/1/user/
    path("<int:user_id>/user/", views.user, name="user"),
    # example: /bookshelf/api/1/user/
    path("api/<int:user_id>/user/", views.user_api, name="user_api"),
    # example: /bookshelf/1/add/
    path("<int:book_id>/add/", views.add_userbook, name="add_userbook"),
    # example: /bookshelf/1/remove/
    path("<int:book_id>/remove/", views.remove_userbook, name="remove_userbook"),
]