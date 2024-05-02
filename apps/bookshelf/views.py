from .models import *
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
    return render(request, "bookshelf/home.html", context)

@login_required(login_url='users:login')
def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
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
    return render(request, "bookshelf/book.html", context)

@login_required(login_url='users:login')
def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "bookshelf/author.html", {"author": author})

@login_required(login_url='users:login')
def user(request, user_id):
    user = request.user
    deleted_at = UserBook.objects.filter(user_id=user.id).values_list('deleted_at')
    user_books = UserBook.objects.filter(
        Q(user_id=user.id) & 
        (Q(created_at__gt=F('deleted_at')) | Q(deleted_at__isnull=True))
    )
    context = {
        "user": user,
        "user_books": user_books
    }
    return render(request, "bookshelf/user.html", context)

def like_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        user = request.user
        if user in book.liked.all():
            book.liked.remove(user)
            like_value = 'unlike'
        else:
            book.liked.add(user)
            like_value = 'like'
        
        like, created = LikedBook.objects.get_or_create(user=user, book=book)
        like.value = 'Unlike' if like.value == 'Like' else 'Like'
        like.save()

        # data = {'value': like.value}
        # return JsonResponse(data)
    return HttpResponseRedirect(reverse("bookshelf:book", args=(book_id,)))



# def user_api(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     # user_books = UserBook.objects.filter(user=user)
#     serializer = UserSerializer(user)
#     return JsonResponse(serializer.data, safe=False)

# def author_api(request, author_id):
#     author = get_object_or_404(Author, pk=author_id)
#     serializer = AuthorSerializer(author)
#     return JsonResponse(serializer.data)

# def book_api(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)
#     serializer = BookSerializer(book)
#     return JsonResponse({'book': serializer.data})

# @login_required(login_url='users:login')
# @api_view(['GET'])
# def home_api(request):
#     if request.method == 'GET':
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return JsonResponse({"books": serializer.data})