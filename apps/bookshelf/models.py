from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    published_at = models.DateField()
    isbn = models.CharField(max_length=13, null=True)
    image_url_s = models.URLField(null=True)
    image_url_m = models.URLField(null=True)
    image_url_l = models.URLField(null=True)
    def __str__(self):
        return self.title

        class Meta:
            ordering = ['title']

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} - {self.book}"