from django import forms
from .models import User


class UserForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "password",
            "phone",
            "birthday",
            "gender",
            "image",
        ]
