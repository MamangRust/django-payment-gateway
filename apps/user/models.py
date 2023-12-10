from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.shared.models import TimeStampedModel
from .manager import MyUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    noc_transfer = models.CharField(max_length=20, default="0")

    phone = models.CharField(max_length=15, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    image = models.ImageField(upload_to="user_images/", null=True, blank=True)

    is_staff = models.BooleanField(
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
