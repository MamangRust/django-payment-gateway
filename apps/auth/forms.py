from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=30,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-xl",
                "placeholder": "Email",
                "data-parsley-required": "true",
            }
        ),
    )
    password = forms.CharField(
        max_length=30,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-xl",
                "placeholder": "Password",
                "data-parsley-required": "true",
            }
        ),
    )


class RegisterForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-xl", "placeholder": "Name"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control form-control-xl", "placeholder": "Email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-xl", "placeholder": "Password"}
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-xl",
                "placeholder": "Confirm Password",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
