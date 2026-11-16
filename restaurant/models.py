from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    inventory = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['id']

    def get_item(self):
        return f'{self.title} : {self.price}'

    def __str__(self):
        return self.get_item()

class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    booking_date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')

    class Meta:
        ordering = ['booking_date','id']

    def __str__(self):
        return f'{self.name} — {self.booking_date}'
