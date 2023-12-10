from django.db import models
from apps.shared.models import TimeStampedModel
from apps.user.models import User


# Create your models here.
class Saldo(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_balance = models.BigIntegerField()
    withdraw_amount = models.BigIntegerField(default=0)
    withdraw_time = models.DateTimeField(null=True, blank=True)
