from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from django.views import View
from apps.user.models import User
from .models import Saldo
from .forms import SaldoForm
from apps.shared.rupiah import rupiah_formatter


# Create your views here.
class SaldoListView(View):
    def get(self, request):
        find_balance = Saldo.objects.values(
            "id",
            "user_id",
            "user__email",
            "user__noc_transfer",
            "total_balance",
            "created_at",
        )

        new_balance_users = [
            {
                "saldo_history": {
                    "saldo_id": balance["id"],
                    "user_id": balance["user_id"],
                    "email": balance["user__email"],
                    "kode_transfer": balance["user__noc_transfer"],
                    "jumlah_uang": rupiah_formatter(str(balance["total_balance"])),
                    "created_at": balance["created_at"],
                }
            }
            for balance in find_balance
        ]

        return render(
            request=request,
            template_name="admin/saldo/index.html",
            context={"saldo": new_balance_users},
        )


class SaldoCreateView(View):
    def get(self, request):
        form = SaldoForm()

        return render(
            request=request,
            template_name="admin/saldo/create.html",
            context={"form": form},
        )

    def post(self, request):
        form = SaldoForm(request.POST)

        if form.is_valid():
            total_balance = form.cleaned_data["total_balance"]
            user_id = form.cleaned_data["user"].id

            if total_balance <= 49000:
                return JsonResponse(
                    {"status": 403, "message": "Minimum saldo Rp 50.000"}, status=403
                )

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse(
                    {
                        "status": 404,
                        "message": "User ID does not exist. Adding saldo failed.",
                    },
                    status=404,
                )

            if Saldo.objects.filter(user=user).exists():
                return JsonResponse(
                    {
                        "status": 409,
                        "message": "Saldo for this user already exists. Adding saldo failed.",
                    },
                    status=409,
                )

            saldo_instance = Saldo(
                user=user, total_balance=total_balance, created_at=datetime.now()
            )
            saldo_instance.save()

            return JsonResponse(
                {"status": 200, "message": "Saldo added successfully"}, status=200
            )

        else:
            return JsonResponse({"status": 400, "errors": form.errors}, status=400)


class SaldoResultView(View):
    def get(self, request, id):
        try:
            find_balance = Saldo.objects.filter(user__id=id).values(
                "id",
                "user__id",
                "user__email",
                "user__noc_transfer",
                "total_balance",
                "created_at",
            )

            if not find_balance.exists():
                return JsonResponse(
                    {
                        "status": 200,
                        "method": request.method,
                        "message": "User ID does not exist",
                    },
                    status=200,
                )

            new_balance_users = {
                "saldo_history": {
                    "saldo_id": find_balance[0]["id"],
                    "user_id": find_balance[0]["user__id"],
                    "email": find_balance[0]["user__email"],
                    "kode_transfer": find_balance[0]["user__noc_transfer"],
                    "jumlah_uang": rupiah_formatter(
                        str(find_balance[0]["total_balance"])
                    ),
                    "created_at": find_balance[0]["created_at"],
                }
            }

            return render(
                request=request,
                template_name="admin/saldo/result.html",
                context={"saldo": new_balance_users},
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": 500,
                    "method": request.method,
                    "message": f"Error: {str(e)}",
                },
                status=500,
            )


class SaldoEditView(View):
    def get(self, request, id):
        try:
            saldo_instance = get_object_or_404(Saldo, pk=id)
            form = SaldoForm(
                initial={
                    "user": saldo_instance.user.pk if saldo_instance.user else None,
                    "total_balance": saldo_instance.total_balance,
                    "withdraw_amount": saldo_instance.withdraw_amount,
                }
            )

            return render(
                request=request,
                template_name="admin/saldo/edit.html",
                context={"form": form, "saldo": saldo_instance},
            )

        except Saldo.DoesNotExist:
            return JsonResponse(
                {
                    "status": 404,
                    "method": request.method,
                    "message": "Saldo data not found",
                },
                status=404,
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": 500,
                    "method": request.method,
                    "message": f"Error: {str(e)}",
                },
                status=500,
            )

    def post(self, request, id):
        try:
            saldo = Saldo.objects.get(id=id)
            form = SaldoForm(request.POST, initial=saldo)
            if form.is_valid():
                user_id = form.cleaned_data["user"]
                total_balance = form.cleaned_data["total_balance"]
                withdraw_amount = form.cleaned_data["withdraw_amount"]

                if total_balance <= 49000:
                    return JsonResponse(
                        {
                            "status": 403,
                            "method": request.method,
                            "message": "Minimum balance Rp 50.000",
                        },
                        status=403,
                    )

                saldo.user = user_id
                saldo.total_balance = total_balance
                saldo.updated_at = datetime.now()
                saldo.withdraw_amount = withdraw_amount
                saldo.save()

                return JsonResponse(
                    {
                        "status": 200,
                        "method": request.method,
                        "message": "Update saldo data successfully",
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {"status": 400, "method": request.method, "errors": form.errors},
                    status=400,
                )

        except Exception as e:
            return JsonResponse(
                {
                    "status": 500,
                    "method": request.method,
                    "message": f"Error: {str(e)}",
                },
                status=500,
            )


class SaldoDeleteView(View):
    def delete(self, request, id):
        try:
            saldo_instance = Saldo.objects.get(id=id)
            saldo_instance.delete()

            return JsonResponse(
                {
                    "status": 200,
                    "method": request.method,
                    "message": "Delete saldo data successfully",
                },
                status=200,
            )

        except Saldo.DoesNotExist:
            return JsonResponse(
                {
                    "status": 404,
                    "method": request.method,
                    "message": "User ID or saldo ID does not exist, delete data saldo failed",
                },
                status=404,
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": 500,
                    "method": request.method,
                    "message": f"Error: {str(e)}",
                },
                status=500,
            )
