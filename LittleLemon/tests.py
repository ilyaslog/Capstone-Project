from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, MenuItem, Booking

class MenuItemTests(APITestCase):
    def setUp(self):
        # Créer un utilisateur manager
        self.manager_group = Group.objects.create(name='Manager')
        self.manager = User.objects.create_user(username='manager', password='manager123')
        self.manager.groups.add(self.manager_group)
        
        # Créer une catégorie
        self.category = Category.objects.create(name='Plats', description='Plats principaux')
        
        # Créer un menu item
        self.menu_item = MenuItem.objects.create(
            name='Pizza',
            description='Pizza margherita',
            price=12.99,
            category=self.category
        )

    def test_create_menu_item(self):
        self.client.force_authenticate(user=self.manager)
        data = {
            'name': 'Burger',
            'description': 'Burger au fromage',
            'price': 9.99,
            'category': self.category.id
        }
        response = self.client.post('/api/menu-items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)

class BookingTests(APITestCase):
    def setUp(self):
        # Créer un utilisateur normal
        self.user = User.objects.create_user(username='user', password='user123')
        
        # Créer une réservation
        self.booking = Booking.objects.create(
            user=self.user,
            date='2024-05-21',
            time='19:00',
            guests=4
        )

    def test_create_booking(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'date': '2024-05-22',
            'time': '20:00',
            'guests': 2
        }
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2) 