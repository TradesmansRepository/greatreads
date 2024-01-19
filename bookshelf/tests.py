from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from .models import Book, Author, UserBook
from django.urls import reverse
from datetime import datetime

class basicAuthTestCase(TestCase):
    def setUp(self):
        u = User.objects.create(id=1, username='jammie', password='password')

    def test_user_can_login(self):
        c = Client()
        u = User.objects.get(id=1)
        response = c.post("/bookshelf/login/", {"username": u.username, "password": u.password}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_can_logout(self):
        c = Client()
        u = User.objects.get(id=1)
        response = c.post("/bookshelf/logout/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        c = Client()
        response = c.post("/bookshelf/register/", {"username": "jammie", "password1": "password", "password2": "password"}, follow=True)
        self.assertEqual(response.status_code, 200)


class UserBookTestCase(TestCase):
    def setUp(self):
        User.objects.create(id=1, username='jammie', password='password')
        Author.objects.create(id=1, first_name='Dave')
        Book.objects.create(id=1, published_at='1995-08-09', author=Author.objects.first())

    def test_user_can_add_book(self):
        c = Client()
        book = Book.objects.get(id=1)
        user = User.objects.get(id=1)
        c.force_login(user)
        url = reverse('add_userbook', args=(book.id,))
        response = c.post(url, {"user": user.id, "book": book.id})
        self.assertEqual(UserBook.objects.filter(id=1).exists(), True)
        self.assertEqual(UserBook.objects.get(id=1).created_at.replace(microsecond=0), datetime.now().replace(microsecond=0))

    def test_userbook_not_duplicated_if_already_exists(self):
        c = Client()
        book = Book.objects.get(id=1)
        user = User.objects.get(id=1)
        c.force_login(user)
        userbook = UserBook.objects.create(id=1, user=user, book=book)
        url = reverse('add_userbook', args=(book.id,))
        response = c.post(url, {"user": user.id, "book": book.id}, follow=True)
        self.assertEqual(UserBook.objects.filter(id=1).count(), 1)
