from django.utils import timezone
from rest_framework import serializers
from .models import Menu, Booking

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','title','price','inventory']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id','name','no_of_guests','booking_date','user']
        read_only_fields = ['user']

    def validate_booking_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Choose a future booking date and time.')
        return value
