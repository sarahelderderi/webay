from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    item_pic = models.ImageField(upload_to='webay/media/item_pics')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_datetime = models.DateTimeField('%d/%m/%Y %H:%M:%S')
    end_datetime = models.DateTimeField('%d/%m/%Y %H:%M:%S')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_datetime = models.DateTimeField('%d/%m/%Y %H:%M:%S')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")

    def __str__(self):
        return self.item.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField()
    profile_pic = models.ImageField(default='default.jpg', upload_to='webay/media/profile_pics')
    address = models.CharField(max_length=255)
    mobile_regex = RegexValidator(regex=r'^0\d{10}$', message='Mobile number must be a valid 11 digit UK number.')
    mobile = models.CharField(validators=[mobile_regex], max_length=11)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    message = models.TextField()
    email_sent = models.BooleanField()
    read_message = models.BooleanField()
