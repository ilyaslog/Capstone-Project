from django.test import TestCase
from django.contrib.auth.models import User
from .models import Menu, Booking, Category

class MenuModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Main', description='Main dishes')
        self.menu = Menu.objects.create(name='Pizza', description='Cheese pizza', price=10.99, category=self.category)

    def test_menu_creation(self):
        self.assertEqual(self.menu.name, 'Pizza')
        self.assertEqual(self.menu.price, 10.99)

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.booking = Booking.objects.create(user=self.user, date='2024-01-01', time='18:00', guests=2)

    def test_booking_creation(self):
        self.assertEqual(self.booking.guests, 2)
        self.assertEqual(self.booking.user.username, 'testuser') 