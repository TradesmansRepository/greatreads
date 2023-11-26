from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Book, Author

def say_hello(request):
    x = 1 
    y = 2
    return render(request, 'hello.html', { 'name': 'plooby'})

def index(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    context = {
        "books": books,
        "authors": authors
    }
    return render(request, "bookshelf/index.html", context)

def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "bookshelf/book.html", {"book": book})

def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "bookshelf/author.html", {"author": author})