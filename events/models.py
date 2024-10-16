# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions for each of their groups.')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True, help_text='Specific permissions for this user')

    def __str__(self):
        return self.username

class Organizer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=40, default='Unknown')
    last_name = models.CharField(max_length=40, default='Unknown')
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(unique=True)

class Attendee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=40, default='Unknown')
    last_name = models.CharField(max_length=40, default='Unknown')
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(unique=True)

class Event(models.Model):
    title = models.CharField(max_length=200)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    venue = models.CharField(max_length=200)
    date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    info = models.TextField()
    time = models.TimeField()
    category = models.CharField(max_length=100, choices=(
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('entertainment', 'Entertainment'),
        ('tourism', 'Tourism and Wildlife'),
        ('business', 'Business'),
        ('education', 'Educational or Academic'),
        ('counselling', 'Counselling and Therapy'),
    ))
    picture = models.ImageField(upload_to='media/event_pictures/', blank=True, null=True)

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    attendee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=(
        ('paypal', 'PayPal'),
        ('mpesa', 'M-Pesa'),
    ))
    confirmation_sent = models.BooleanField(default=False)

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    tickets = models.ManyToManyField(Ticket, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)

class MpesaTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    transaction_code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    event_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.event_name} - {self.amount}"