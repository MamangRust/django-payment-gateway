from django import forms

from apps.user.models import User


class SaldoForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Select user"}
        ),
    )
    total_balance = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter total balance"}
        ),
    )
    withdraw_amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter withdraw amount"}
        ),
    )
