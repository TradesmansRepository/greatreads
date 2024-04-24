from .models import Book, Author, UserBook
from .serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.http import JsonResponse
from django.db.models import F, Q

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
    # is book exists in user's bookshelf then true
    user = request.user
    userbook = UserBook.objects.filter(Q(user=user) & Q(book=book) & (Q(created_at__gt=F('deleted_at')) | Q(deleted_at__isnull=True)))
    if userbook:
        is_book_in_bookshelf = True
    else:
        is_book_in_bookshelf = False
    context = {
        "book": book,
        "is_book_in_bookshelf": is_book_in_bookshelf
    }
    return render(request, "book.html", context)

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
        # userbook = UserBook.objects.get(book=book, user=user)
        userbook = UserBook.objects.get(Q(book=book) & Q(user_id=user.id) & (Q(created_at__gt=F('deleted_at')) | Q(deleted_at__isnull=True)))
    except (KeyError, UserBook.DoesNotExist):
        u = UserBook(user=user, book=book, created_at=datetime.now())
        u.save()
        messages.success(request, book.title + ' was added to your bookshelf')
    except MultipleObjectsReturned:
        messages.error(request, "this book is already on your bookshelf_1")
    else:
        messages.error(request, "this book is already on your bookshelf_2")
    return HttpResponseRedirect(reverse("user", args=(user.id,)))

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
    deleted_at = UserBook.objects.filter(user=user).values_list('deleted_at')
    user_books = UserBook.objects.filter(Q(user_id=user.id) & (Q(created_at__gt=F('deleted_at')) | Q(deleted_at__isnull=True)))

    context = {
        "user": user,
        "user_books": user_books
    }
    return render(request, "user.html", context)

def user_api(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # user_books = UserBook.objects.filter(user=user)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, safe=False)