from django.shortcuts import redirect, render
from apps.user.models import User
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "auth/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("dashboard")
        return render(request, "auth/login.html", {"form": form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "auth/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=name, email=email, password=password
            )
            user.save()
            return redirect("login")
        return render(request, "auth/register.html", {"form": form})


@login_required(login_url="/auth/login")
def profile(request):
    return render(
        request=request,
        template_name="admin/profile/index.html",
        context={"request": request},
    )
