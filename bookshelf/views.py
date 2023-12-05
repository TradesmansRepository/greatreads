from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Book, Author
from .forms import CreatUserForm

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
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
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or password is incorrect.')

        context = {}
        return render(request, 'bookshelf/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    context = {
        "books": books,
        "authors": authors
    }
    return render(request, "bookshelf/index.html", context)

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
    return render(request, "bookshelf/book.html", {"book": book})

@login_required(login_url='login')
def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "bookshelf/author.html", {"author": author})

@login_required(login_url='login')
def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    books = UserBooks.objects.filter(user_id)
    context = {
        "user": user,
        "books": books
    }
    return render(request, "bookshelf/user.html", {"user": user})