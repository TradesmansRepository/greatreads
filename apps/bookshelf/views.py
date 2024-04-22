from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Book, Author, UserBook
from datetime import datetime
from .serializers import *
from django.http import JsonResponse
from rest_framework.decorators import api_view

@login_required(login_url='users:login')
def home(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    paginator = Paginator(books, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "books": books,
        "authors": authors,
        "page_obj": page_obj
    }
    return render(request, "home.html", context)

@login_required(login_url='users:login')
@api_view(['GET'])
def home_api(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse({"books": serializer.data})

@login_required(login_url='users:login')
def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "book.html", {"book": book,})

def book_api(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    serializer = BookSerializer(book)
    return JsonResponse({'book': serializer.data})

@login_required(login_url='users:login')
def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "author.html", {"author": author})

def author_api(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    serializer = AuthorSerializer(author)
    return JsonResponse(serializer.data)

def add_userbook(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    try:
        userbook = UserBook.objects.get(book=book, user=user)
    except (KeyError, UserBook.DoesNotExist):
        u = UserBook(user=user, book=book, created_at=datetime.now())
        u.save()
        messages.success(request, book.title + ' was added to your bookshelf')
    except MultipleObjectsReturned:
        messages.error(request, "this book is already on your bookshelf")
    else:
        messages.error(request, "this book is already on your bookshelf")
    return HttpResponseRedirect(reverse("home"))

def remove_userbook(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    try:
        userbook = UserBook.objects.get(book=book, user=user)
    except (KeyError, UserBook.DoesNotExist):
        messages.error(request, "this book is not on your bookshelf")
    else:
        userbook.deleted_at = datetime.now()
        userbook.save()
        messages.success(request, book.title + ' was removed from your bookshelf')
    return HttpResponseRedirect(reverse("home"))


@login_required(login_url='users:login')
def user(request, user_id):
    user = request.user
    user_books = UserBook.objects.filter(user=user)
    for user_book in user_books:
        if user_book.deleted_at is None:
            return user_book
        elif user_book.created_at > user_book.deleted_at:
            return userbook

    # user_books = user_books.filter(created_at__lte=user_books.deleted_at)
    # print("book id = ", user_books[0].book.id, "userbook user id = ", user_books[0].user.id, "userbook id = ", user_books[0].id, "request user id = ", user.id, "user id = ", user_id, user_books[0].created_at)
    context = {
        "user": user,
        "user_books": user_book
    }
    return render(request, "user.html", context)

def user_api(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # user_books = UserBook.objects.filter(user=user)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, safe=False)