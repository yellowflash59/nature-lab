
from django.db import models
from django.contrib.auth.models import AbstractUser
from advisor.models import Advisor
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class AdvisorBooking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    booking_time = models.DateTimeField()
