from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, MenuItem, Table, Booking
from .serializers import (
    CategorySerializer, MenuItemSerializer,
    TableSerializer, BookingSerializer
)

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = MenuItem.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        date = request.query_params.get('date', None)
        time = request.query_params.get('time', None)
        
        if not date or not time:
            return Response(
                {"error": "Date and time parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        reserved_tables = Booking.objects.filter(
            date=date,
            time=time,
            status__in=['confirmed', 'pending']
        ).values_list('table_id', flat=True)
        
        available_tables = self.queryset.exclude(id__in=reserved_tables)
        serializer = self.get_serializer(available_tables, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        table_id = self.request.data.get('table')
        date = self.request.data.get('date')
        time = self.request.data.get('time')
        
        # Check if table is available
        if Booking.objects.filter(
            table_id=table_id,
            date=date,
            time=time,
            status__in=['confirmed', 'pending']
        ).exists():
            raise serializers.ValidationError(
                "This table is already booked for the selected time"
            )
        
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == 'cancelled':
            return Response(
                {"error": "Booking is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
