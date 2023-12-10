from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from .forms import UserForm


class UserListView(LoginRequiredMixin, View):
    redirect_field_name = "/auth/login"

    def get(self, request):
        users = User.objects.all()
        return render(
            request=request,
            template_name="admin/user/index.html",
            context={"users": users},
        )


class UserCreateView(LoginRequiredMixin, View):
    redirect_field_name = "/auth/login"

    def get(self, request):
        form = UserForm()
        return render(
            request,
            "admin/user/create.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])
            user.save()
            return JsonResponse({"message": "User created successfully"}, status=201)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)


class UserEditView(LoginRequiredMixin, View):
    redirect_field_name = "/auth/login"

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        form = UserForm(instance=user)

        return render(
            request,
            "admin/user/edit.html",
            {
                "title": "Edit User",
                "user": user,
                "form": form,
            },
        )

    def post(self, request, id):
        user = get_object_or_404(User, pk=id)
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user_instance = form.save(commit=False)
            if form.cleaned_data.get("password"):
                user_instance.password = make_password(form.cleaned_data["password"])
            user_instance.save()
            return JsonResponse({"message": "User updated successfully"}, status=201)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)


class UserDeleteView(LoginRequiredMixin, View):
    redirect_field_name = "/auth/login"

    def delete(self, request, id):
        user = get_object_or_404(User, pk=id)
        user.delete()

        return JsonResponse({"message": "User deleted successfully"})
