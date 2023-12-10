from django.db import models
from apps.shared.models import TimeStampedModel
from apps.user.models import User
from apps.shared.uniquenumber import unique_order_number


payment_rules = [
    ("alfamart", "Alfamart"),
    ("indomart", "Indomart"),
    ("lawson", "Lawson"),
    ("dana", "Dana"),
    ("ovo", "OVO"),
    ("gopay", "GoPay"),
    ("linkaja", "LinkAja"),
    ("jenius", "Jenius"),
    ("fastpay", "FastPay"),
    ("kudo", "Kudo"),
    ("bri", "BRI"),
    ("mandiri", "Mandiri"),
    ("bca", "BCA"),
    ("bni", "BNI"),
    ("bukopin", "Bukopin"),
    ("e-banking", "E-Banking"),
    ("visa", "Visa"),
    ("mastercard", "Mastercard"),
    ("discover", "Discover"),
    ("american express", "American Express"),
    ("paypal", "PayPal"),
]


# Create your models here.
class Topups(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topup_no = models.CharField(default=unique_order_number(), max_length=255)
    topup_amount = models.BigIntegerField()
    topup_method = models.CharField(max_length=255, choices=payment_rules)
    topup_time = models.DateTimeField()
