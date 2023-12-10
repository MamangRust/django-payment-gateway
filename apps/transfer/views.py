from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Transfer
from apps.user.models import User
from datetime import datetime
from .forms import TransferForm
from django.db.models import Sum, F
from apps.shared.rupiah import rupiah_formatter
from apps.shared.dateformat import date_format


# Create your views here.
class TransferResultsView(View):
    def get(self, request):
        find_transfer_saldo_from = (
            Transfer.objects.values(
                "transfer_from__id",
                "transfer_from__email",
                "transfer_from__noc_transfer",
            )
            .annotate(
                total_transfer_amount=Sum("transfer_amount"),
                transfer_from=F("transfer_from__id"),
                transfer_to=F("transfer_to__id"),
            )
            .order_by("transfer_from__id")
        )

        if not find_transfer_saldo_from.exists():
            return render(
                request,
                "admin/transfer/index.html",
                {"status": 200, "message": "Data does not exist"},
            )

        transfer_saldo = []
        for val in find_transfer_saldo_from:
            find_transfer_saldo_to = (
                Transfer.objects.filter(
                    transfer_to=val["transfer_to"],
                    transfer_from=val["transfer_from"],
                )
                .values(
                    "transfer_to__id",
                    "transfer_id",
                    "transfer_to__email",
                    "transfer_to__noc_transfer",
                    "transfer_amount",
                    "transfer_time",
                )
                .annotate(
                    transfer_id=F("id"),
                    email=F("transfer_to__email"),
                    noc_transfer=F("transfer_to__noc_transfer"),
                )
                .order_by("-transfer_time")
            )

            new_find_saldo_to = []
            for transfer in find_transfer_saldo_to:
                new_find_saldo_to.append(
                    {
                        "transfer_id": transfer["transfer_id"],
                        "email": transfer["email"],
                        "kode_transfer": transfer["noc_transfer"],
                        "nominal_transfer": rupiah_formatter(
                            str(transfer["transfer_amount"])
                        ),
                        "tanggal_transfer": date_format(
                            transfer["transfer_time"]
                        ).strftime("%c"),
                    }
                )

            transfer_saldo.append(
                {
                    "transfer_history": {
                        "user_id": val["transfer_from__id"],
                        "email": val["transfer_from__email"],
                        "kode_transfer": val["transfer_from__noc_transfer"],
                        "total_nominal_transfer": rupiah_formatter(
                            str(val["total_transfer_amount"])
                        ),
                        "total_transfer": new_find_saldo_to,
                    }
                }
            )

        return render(
            request,
            "admin/transfer/index.html",
            {"data": transfer_saldo},
        )


class TransferResultView(View):
    def get(self, request, id):
        find_transfer_saldo_from = (
            Transfer.objects.values(
                "transfer_from__id",
                "transfer_from__email",
                "transfer_from__noc_transfer",
                "transfer_from",
                "transfer_to",
            )
            .annotate(total_transfer_amount=Sum("transfer_amount"))
            .filter(transfer_from=id)
            .order_by("transfer_from__id")
        )

        check_user_id = User.objects.filter(id=id).values("email")
        if not find_transfer_saldo_from and check_user_id:
            return JsonResponse(
                {
                    "status": 200,
                    "method": "GET",
                    "message": f"{check_user_id[0]['email']} you never transferred money to other people",
                }
            )

        transfer_saldo = []

        for val in find_transfer_saldo_from:
            find_saldo_to = (
                Transfer.objects.filter(
                    transfer_to=val["transfer_to"], transfer_from=val["transfer_from"]
                )
                .values(
                    "transfer_to",
                    "id",
                    "transfer_to__email",
                    "transfer_to__noc_transfer",
                    "transfer_amount",
                    "transfer_time",
                )
                .order_by("-transfer_time")
            )

            new_find_saldo_to = []

            for to_val in find_saldo_to:
                new_find_saldo_to.append(
                    {
                        "transfer_id": to_val["id"],
                        "email": to_val["transfer_to__email"],
                        "kode_transfer": to_val["transfer_to__noc_transfer"],
                        "nominal_transfer": rupiah_formatter(
                            str(to_val["transfer_amount"])
                        ),
                        "tanggal_transfer": to_val["transfer_time"].strftime("%c"),
                    }
                )

            transfer_saldo.append(
                {
                    "transfer_history": {
                        "user_id": val["transfer_from__id"],
                        "email": val["transfer_from__email"],
                        "kode_transfer": val["transfer_from__noc_transfer"],
                        "total_nominal_transfer": rupiah_formatter(
                            str(val["total_transfer_amount"])
                        ),
                        "total_transfer": new_find_saldo_to,
                    }
                }
            )

        return render(
            request=request,
            template_name="admin/transfer/result.html",
            context={"data": transfer_saldo},
        )


class TransferCreateView(View):
    def get(self, request):
        form = TransferForm()
        return render(
            request=request,
            template_name="admin/transfer/create.html",
            context={"form": form},
        )

    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = Transfer()
            transfer.transfer_from = form.cleaned_data["transfer_from"]
            transfer.transfer_to = form.cleaned_data["transfer_to"]
            transfer.transfer_amount = form.cleaned_data["transfer_amount"]

            if transfer.transfer_from.saldo < transfer.transfer_amount:
                return JsonResponse({"status": 403, "message": "Insufficient balance"})

            transfer.transfer_from.saldo -= transfer.transfer_amount
            transfer.transfer_to.saldo += transfer.transfer_amount
            transfer.transfer_from.save()
            transfer.transfer_to.save()

            transfer.save()
            return JsonResponse({"status": 201, "message": "Transfer successful"})

        return JsonResponse({"status": 400, "message": "Invalid data"})


class TransferEditView(View):
    def get(self, request, id):
        transfer = get_object_or_404(Transfer, pk=id)
        form = TransferForm(
            initial={
                "transfer_from": transfer.transfer_from,
                "transfer_to": transfer.transfer_to,
                "transfer_amount": transfer.transfer_amount,
            }
        )
        return render(
            request=request,
            template_name="transfer_edit.html",
            context={"form": form, "transfer": transfer},
        )

    def post(self, request, id):
        transfer = get_object_or_404(Transfer, pk=id)
        form = TransferForm(
            request.POST,
            initial={
                "transfer_from": transfer.transfer_from,
                "transfer_to": transfer.transfer_to,
                "transfer_amount": transfer.transfer_amount,
            },
        )
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer_from = form.cleaned_data["transfer_from"]
            transfer_to = form.cleaned_data["transfer_to"]
            transfer_amount = form.cleaned_data["transfer_amount"]

            if transfer_from.saldo < transfer_amount:
                return JsonResponse({"status": 403, "message": "Insufficient balance"})

            transfer_from.saldo -= transfer_amount
            transfer_to.saldo += transfer_amount
            transfer_from.save()
            transfer_to.save()

            transfer.save()
            return JsonResponse({"status": 200, "message": "Transfer updated"})

        return JsonResponse({"status": 400, "message": "Invalid data"})


class TransferDeleteView(View):
    def post(self, request, id):
        try:
            transfer = Transfer.objects.get(id=id)
            transfer.delete()
            return JsonResponse(
                {
                    "status": 200,
                    "method": "POST",
                    "message": "Delete data transfer successfully",
                }
            )
        except Transfer.DoesNotExist:
            return JsonResponse(
                {
                    "status": 404,
                    "method": "POST",
                    "message": "Transfer record not found",
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": 500,
                    "method": "POST",
                    "message": f"Failed to delete transfer record: {str(e)}",
                }
            )
