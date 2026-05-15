from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager

class User(AbstractUser):
    username = models.CharField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    objects = UserManager()

