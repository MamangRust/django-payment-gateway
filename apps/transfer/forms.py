from django import forms

from apps.user.models import User


class TransferForm(forms.Form):
    transfer_from = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    transfer_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    transfer_amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
