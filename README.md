# Restaurant Booking System

A simple restaurant booking system.

## Setup

1. Install Python 3.8 or higher
2. Install MySQL
3. Create virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install requirements:
   ```
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create superuser:
   ```
   python manage.py createsuperuser
   ```
7. Run server:
   ```
   python manage.py runserver
   ```

## Features

- Menu management
- Table booking
- User registration
- Basic authentication

## API Endpoints

- /api/categories/ - Menu categories
- /api/items/ - Menu items
- /api/tables/ - Restaurant tables
- /api/bookings/ - Table bookings
