from django import forms
from .models import Topups
from apps.user.models import User

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


class TopUpForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    topup_amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    topup_method = forms.ChoiceField(
        choices=payment_rules,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
