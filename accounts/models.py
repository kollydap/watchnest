from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # UUID as primary key
    email = models.EmailField(unique=True)

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.CharField(max_length=500)
    device = models.CharField(max_length=250)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    loyalty_points = models.IntegerField(default=0)
    registration_ip = models.GenericIPAddressField(null=True, blank=True)
    online_status = models.CharField(
        max_length=20,
        choices=[
            ("ONLINE", "Online"),
            ("OFFLINE", "Offline"),
        ],
        default="ONLINE",
    )
    account_status = models.CharField(
        max_length=20,
        choices=[
            ("ACTIVE", "Active"),
            ("SUSPENDED", "Suspended"),
            ("BANNED", "Banned"),
        ],
        default="ACTIVE",
    )

    def __str__(self):
        return self.username
