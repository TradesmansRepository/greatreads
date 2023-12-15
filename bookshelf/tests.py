from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Book, Author

class UserBookTestCase(TestCase):
    def setUp(self):
        u = User.objects.create(id=1, username='jammie', password='password')
        Author.objects.create(id=1, first_name='Dave')
        Book.objects.create(id=1, published_at='1995-08-09', author=Author.objects.first())

    def test_user_can_login(self):
        c = Client()
        u = User.objects.get(id=1)
        response = c.post("/bookshelf/login/", {"username": u.username, "password": u.password}, follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_user_can_get_own_page(self):
        u = User.objects.get(id=1)
        response = self.client.get("/bookshelf/1/user/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_get_others_page(self):
        u = User.objects.get(id=1)
        response = self.client.get("/bookshelf/2/user/", follow=True)
        self.assertEqual(response.status_code, 403)