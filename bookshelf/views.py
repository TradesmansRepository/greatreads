from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import MultipleObjectsReturned

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Book, Author, UserBook
from .forms import CreatUserForm

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreatUserForm()
        if request.method == 'POST':
            form = CreatUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'bookshelf/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect.')

        context = {}
        return render(request, 'bookshelf/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    context = {
        "books": books,
        "authors": authors
    }
    return render(request, "bookshelf/home.html", context)

@login_required(login_url='login')
def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "bookshelf/book.html", {"book": book,})

def add_userbook(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    try:
        userbook = UserBook.objects.get(book=book, user=user)
    except (KeyError, UserBook.DoesNotExist):
        print('does not exist')
        u = UserBook(user=user, book=book)
        u.save()
        messages.success(request, book + ' was added to your bookshelf')
    except MultipleObjectsReturned:
        print('multiple already exist')
        messages.error(request, "this book is already on your bookshelf")
    else:
        print('already exists')
        messages.error(request, "this book is already on your bookshelf")
    return HttpResponseRedirect(reverse("home"))

@login_required(login_url='login')
def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "bookshelf/author.html", {"author": author})

@login_required(login_url='login')
def user(request, user_id):
    user = request.user
    user_books = UserBook.objects.filter(user=user)
    context = {
        "user": user,
        "user_books": user_books
    }
    return render(request, "bookshelf/user.html", context)