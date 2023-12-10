from django import forms
from .models import Withdraw
from apps.user.models import User


class WithdrawForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    Withdraw_amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    withdraw = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Withdraw
        fields = "__all__"
