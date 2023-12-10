from django.db import models
from apps.shared.models import TimeStampedModel
from apps.user.models import User


# Create your models here.
class Withdraw(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    withdraw_amount = models.BigIntegerField()
    withdraw_time = models.DateTimeField()
