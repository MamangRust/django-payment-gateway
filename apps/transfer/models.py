from django.db import models
from apps.shared.models import TimeStampedModel
from apps.user.models import User


# Create your models here.
class Transfer(TimeStampedModel):
    transfer_from = models.ForeignKey(
        User, related_name="transfer_from", on_delete=models.CASCADE
    )
    transfer_to = models.ForeignKey(
        User, related_name="transfer_to", on_delete=models.CASCADE
    )
    transfer_amount = models.BigIntegerField(default=0)
    transfer_time = models.DateTimeField()
