from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Withdraw
from django.db.models import Sum, F
from django.http import JsonResponse
from apps.user.models import User
from .forms import WithdrawForm
from apps.shared.rupiah import rupiah_formatter
from apps.shared.dateformat import date_format
from apps.saldo.models import Saldo
from datetime import timezone


# Create your views here.
class WithdrawListView(View):
    def get(self, request):
        find_withdraw_amount = (
            Withdraw.objects.values(
                "user__id",
                "user__email",
                "user__noc_transfer",
            )
            .annotate(
                total_withdraw_amount=Sum("withdraw_amount"),
                user_id=F("user__id"),
            )
            .order_by("user__id")
        )

        if not find_withdraw_amount.exists():
            return render(
                request=request,
                template_name="admin/withdraw/index.html",
                context={"data": [], "message": "Data does not exist"},
            )

        withdraw_amount = []
        for val in find_withdraw_amount:
            find_withdraw_history = (
                Withdraw.objects.filter(user__id=val["user__id"])
                .values(
                    "user__id",
                    "user__email",
                    "user__noc_transfer",
                    "withdraw_id",
                    "withdraw_amount",
                    "withdraw_time",
                )
                .annotate(
                    transfer_id=F("withdraw_id"),
                    email=F("user__email"),
                    noc_transfer=F("user__noc_transfer"),
                )
                .order_by("-withdraw_time")
            )

            new_withdraw_history = []
            for withdraw in find_withdraw_history:
                new_withdraw_history.append(
                    {
                        "transfer_id": withdraw["withdraw_id"],
                        "email": withdraw["user__email"],
                        "kode_transfer": withdraw["user__noc_transfer"],
                        "nominal_withdraw": rupiah_formatter(
                            str(withdraw["withdraw_amount"])
                        ),
                        "tanggal_withdraw": date_format(
                            withdraw["withdraw_time"]
                        ).strftime("%c"),
                    }
                )

            withdraw_amount.append(
                {
                    "withdraw_history": {
                        "user_id": val["user__id"],
                        "email": val["user__email"],
                        "kode_transfer": val["user__noc_transfer"],
                        "total_nominal_withdraw": rupiah_formatter(
                            str(val["total_withdraw_amount"])
                        ),
                        "total_withdraw": new_withdraw_history,
                    }
                }
            )

        return render(
            request=request,
            template_name="admin/withdraw/index.html",
            context={"data": withdraw_amount},
        )


class WithdrawResultView(View):
    def get(self, request, id):
        check_user = get_object_or_404(User, pk=id)

        find_withdraw_amount = (
            Withdraw.objects.values(
                "user__id",
                "user__email",
                "user__noc_transfer",
            )
            .annotate(
                total_withdraw_amount=Sum("withdraw_amount"),
                user_id=F("user__id"),
            )
            .filter(user__id=id)
            .order_by("user__id")
        )

        if not find_withdraw_amount.exists():
            return render(
                request,
                "admin/withdraw/result.html",
                {
                    "status": 200,
                    "method": request.method,
                    "message": f"{check_user.email} you never withdraw money",
                },
            )

        withdraw_amount = []
        for val in find_withdraw_amount:
            find_withdraw_history = (
                Withdraw.objects.filter(user__id=val["user__id"])
                .values(
                    "user__id",
                    "user__email",
                    "user__noc_transfer",
                    "withdraw_id",
                    "withdraw_amount",
                    "withdraw_time",
                )
                .annotate(
                    transfer_id=F("withdraw_id"),
                    email=F("user__email"),
                    noc_transfer=F("user__noc_transfer"),
                )
                .order_by("-withdraw_time")
            )

            new_withdraw_history = []
            for withdraw in find_withdraw_history:
                new_withdraw_history.append(
                    {
                        "transfer_id": withdraw["withdraw_id"],
                        "email": withdraw["user__email"],
                        "kode_transfer": withdraw["user__noc_transfer"],
                        "nominal_withdraw": rupiah_formatter(
                            str(withdraw["withdraw_amount"])
                        ),
                        "tanggal_withdraw": date_format(
                            withdraw["withdraw_time"]
                        ).strftime("%c"),
                    }
                )

            withdraw_amount.append(
                {
                    "withdraw_history": {
                        "user_id": val["user__id"],
                        "email": val["user__email"],
                        "kode_transfer": val["user__noc_transfer"],
                        "total_nominal_withdraw": rupiah_formatter(
                            str(val["total_withdraw_amount"])
                        ),
                        "total_withdraw": new_withdraw_history,
                    }
                }
            )

        return render(
            request,
            "admin/withdraw/result.html",
            {
                "status": 200,
                "method": request.method,
                "message": "data already to use",
                "data": withdraw_amount[0],
            },
        )


class WithdrawCreateView(View):
    def get(self, request):
        form = WithdrawForm()
        return render(request, "admin/withdraw/create.html", {"form": form})

    def post(self, request):
        form = WithdrawForm(request.POST)
        if form.is_valid():
            withdraw_amount = form.cleaned_data["withdraw_amount"]
            user_id = form.cleaned_data["user_id"]

            if withdraw_amount <= 49000:
                return JsonResponse(
                    {"status": 403, "message": "Minimum withdraw balance is Rp 50.000"}
                )

            user = User.objects.filter(user_id=user_id).first()
            if not user:
                return JsonResponse(
                    {
                        "status": 404,
                        "message": "User ID does not exist, withdraw failed",
                    }
                )

            saldo = Saldo.objects.filter(user=user).first()
            if saldo.total_balance <= 49000:
                return JsonResponse(
                    {
                        "status": 403,
                        "message": f"{user.email} your balance is insufficient {saldo.total_balance}",
                    }
                )

            withdraw = Withdraw.objects.create(
                user=user, withdraw_amount=withdraw_amount, withdraw_time=timezone.now()
            )

            if withdraw:
                saldo.total_balance -= withdraw_amount
                saldo.save()

                return JsonResponse(
                    {
                        "status": 200,
                        "message": f"Withdraw successful, please check your email {user.email}",
                    }
                )
            else:
                return JsonResponse(
                    {"status": 408, "message": "Withdraw failed, server is busy"}
                )
        else:
            return JsonResponse({"status": 400, "message": "Invalid data"})


class WithdrawEditView(View):
    def get(self, request, id):
        withdraw = get_object_or_404(Withdraw, pk=id)

        form = WithdrawForm(instance=withdraw)
        return render(
            request,
            "admin/withdraw/edit.html",
            {"form": form, "withdraw_id": id},
        )

    def post(self, request, id):
        withdraw = get_object_or_404(Withdraw, pk=id)
        form = WithdrawForm(request.POST, instance=withdraw)
        if form.is_valid():
            withdraw_amount = form.cleaned_data["withdraw_amount"]

            if withdraw_amount <= 49000:
                return JsonResponse(
                    {"status": 403, "message": "Minimum withdraw balance is Rp 50.000"}
                )

            saldo = Saldo.objects.filter(user=withdraw.user).first()
            if saldo.total_balance <= 49000:
                return JsonResponse(
                    {
                        "status": 403,
                        "message": f"{withdraw.user.email} your balance is insufficient {saldo.total_balance}",
                    }
                )

            form.save()

            saldo.total_balance -= withdraw_amount
            saldo.save()

            return JsonResponse(
                {"status": 200, "message": "Withdraw updated successfully"}
            )
        else:
            return JsonResponse({"status": 400, "message": "Invalid data"})


class WithdrawDeleteView(View):
    def post(self, request, id):
        try:
            withdraw_instance = Withdraw.objects.get(id=id)
        except Withdraw.DoesNotExist:
            return JsonResponse(
                {
                    "status": 404,
                    "method": request.method,
                    "message": "withdraw id is not exist, delete data withdraw failed",
                }
            )

        delete_status = withdraw_instance.delete()

        if delete_status:
            return JsonResponse(
                {
                    "status": 200,
                    "method": request.method,
                    "message": "delete data withdraw successfully",
                }
            )
        else:
            return JsonResponse(
                {
                    "status": 408,
                    "method": request.method,
                    "message": "delete data withdraw failed, server is busy",
                }
            )
