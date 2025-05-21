from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Table, Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'image']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'capacity', 'is_available']

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    table = TableSerializer(read_only=True)
    table_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'table', 'table_id', 'date', 'time', 'guests', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        table = Table.objects.get(id=validated_data.pop('table_id'))
        validated_data['table'] = table
        return super().create(validated_data) 