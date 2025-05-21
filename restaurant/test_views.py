from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Menu, Booking, Category
from rest_framework import status
from django.urls import reverse

class MenuViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Main', description='Main dishes')
        self.menu = Menu.objects.create(name='Pizza', description='Cheese pizza', price=10.99, category=self.category)

    def test_list_menu(self):
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BookingViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.booking = Booking.objects.create(user=self.user, date='2024-01-01', time='18:00', guests=2)

    def test_list_bookings(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 