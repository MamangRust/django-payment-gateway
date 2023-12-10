from django.shortcuts import render, get_object_or_404
from .forms import TopUpForm
from .models import Topups
from apps.user.models import User
from django.db.models import Sum
from apps.saldo.models import Saldo
from apps.transfer.models import Transfer
from apps.shared.rupiah import rupiah_formatter
from apps.shared.uniquenumber import unique_order_number
from apps.shared.paymentmethod import payment_method_validator
from datetime import datetime
from django.http import JsonResponse
from django.views import View


# Create your views here.
class TopupListView(View):
    def get(self, request):
        find_topup_amount = (
            Topups.objects.values("user_id", "user__email", "user__noc_transfer")
            .annotate(total_topup_amount=Sum("topup_amount"))
            .order_by("user_id")
        )

        topup_data = []
        for val in find_topup_amount:
            user_topup_history = Topups.objects.filter(user_id=val["user_id"]).order_by(
                "-topup_time"
            )
            topup_history = [
                {
                    "topup_id": h.id,  # Use the correct primary key field name
                    "kode_topup": h.topup_no,
                    "nominal_topup": rupiah_formatter(str(h.topup_amount)),
                    "metode_pembayaran": h.topup_method,
                    "tanggal_topup": h.topup_time.strftime("%c"),
                }
                for h in user_topup_history
            ]

            topup_data.append(
                {
                    "user_id": val["user_id"],
                    "email": val["user__email"],
                    "kode_transfer": val["user__noc_transfer"],
                    "total_nominal_topup": rupiah_formatter(
                        str(val["total_topup_amount"])
                    ),
                    "total_topup": topup_history,
                }
            )

        return render(
            request=request,
            template_name="admin/topup/index.html",
            context={"data": topup_data},
        )


class TopupCreateView(View):
    def get(self, request):
        form = TopUpForm()

        return render(
            request=request,
            template_name="admin/topup/create.html",
            context={"form": form},
        )

    def post(self, request):
        form = TopUpForm(request.POST)
        if form.is_valid():
            topup_amount = form.cleaned_data["topup_amount"]
            topup_method = form.cleaned_data["topup_method"]
            user_id = form.cleaned_data["user"].id

            if topup_amount <= 49000:
                return JsonResponse(
                    {"status": 403, "message": "Minimum topup balance is Rp 50,000"}
                )

            if not payment_method_validator(topup_method):
                return JsonResponse(
                    {"status": 403, "message": "Payment method is not supported"}
                )

            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse(
                    {
                        "status": 400,
                        "message": "User ID does not exist, topup balance failed",
                    }
                )

            topup = Topups.objects.create(
                user=user,
                topup_no=unique_order_number(),
                topup_amount=topup_amount,
                topup_method=topup_method,
                topup_time=datetime.now(),
            )

            saldo_obj, created = Saldo.objects.get_or_create(user=user)
            saldo_obj.total_balance += topup_amount
            saldo_obj.save()

            return JsonResponse({"status": 201, "message": "Topup balance successful"})

        return JsonResponse({"status": 400, "message": "Invalid data"})


class TopupResultView(View):
    def get(self, request, id):
        find_topup_amount = (
            Topups.objects.values("user_id", "user__email", "user__noc_transfer")
            .annotate(total_topup_amount=Sum("topup_amount"))
            .filter(user_id=id)
            .order_by("user_id")
        )

        user = User.objects.filter(id=id).values("email").first()

        if not find_topup_amount and user:
            return JsonResponse(
                {
                    "status": 200,
                    "method": "GET",
                    "message": f"{user['email']} you never topup money",
                }
            )

        topup_history = []
        for val in find_topup_amount:
            topup_amount_history = (
                Topups.objects.filter(user_id=val["user_id"])
                .values(
                    "id",
                    "user_id",
                    "topup_no",
                    "topup_amount",
                    "topup_method",
                    "topup_time",
                )
                .order_by("-topup_time")
            )
            new_topup_amount_history = []
            for history in topup_amount_history:
                new_topup_amount_history.append(
                    {
                        "topup_id": history["id"],
                        "kode_topup": history["topup_no"],
                        "nominal_topup": rupiah_formatter(history["topup_amount"]),
                        "metode_pembayaran": history["topup_method"],
                        "tanggal_topup": history["topup_time"].strftime("%c"),
                    }
                )

            topup_history.append(
                {
                    "user_id": val["user_id"],
                    "email": val["user__email"],
                    "kode_transfer": val["user__noc_transfer"],
                    "total_nominal_topup": rupiah_formatter(val["total_topup_amount"]),
                    "total_topup": new_topup_amount_history,
                }
            )
        print(topup_history)

        return render(
            request=request,
            template_name="admin/topup/result.html",
            context={"data": topup_history},
        )


class TopupEditView(View):
    def get(self, request, id):
        topup = get_object_or_404(Topups, pk=id)
        initial_data = {
            "user": topup.user,
            "topup_amount": topup.topup_amount,
            "topup_method": topup.topup_method,
        }
        form = TopUpForm(initial=initial_data)

        return render(
            request=request,
            template_name="admin/topup/edit.html",
            context={"form": form, "topup": topup},
        )

    def post(self, request, id):
        form = TopUpForm(request.POST)
        if form.is_valid():
            topup_amount = form.cleaned_data["topup_amount"]
            topup_method = form.cleaned_data["topup_method"]
            user_id = form.cleaned_data["user"].id

            if topup_amount <= 49000:
                return JsonResponse(
                    {"status": 403, "message": "Minimum topup balance is Rp 50,000"}
                )

            if not payment_method_validator(topup_method):
                return JsonResponse(
                    {"status": 403, "message": "Payment method is not supported"}
                )

            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse(
                    {
                        "status": 400,
                        "message": "User ID does not exist, topup balance failed",
                    }
                )

            try:
                topup = Topups.objects.get(id=id)
                if topup.user != user:
                    return JsonResponse(
                        {"status": 400, "message": "Topup does not belong to this user"}
                    )

                topup.topup_amount = topup_amount
                topup.topup_method = topup_method
                topup.save()

                saldo_obj, created = Saldo.objects.get_or_create(user=user)
                saldo_obj.total_balance -= topup.topup_amount
                saldo_obj.total_balance += topup_amount
                saldo_obj.save()

                return JsonResponse(
                    {"status": 200, "message": "Topup balance updated successfully"}
                )
            except Topups.DoesNotExist:
                return JsonResponse({"status": 404, "message": "Topup not found"})

        return JsonResponse({"status": 400, "message": "Invalid data"})


class TopupDeleteView(View):
    def post(self, request, id):
        try:
            topup = Topups.objects.get(id=id)
        except Topups.DoesNotExist:
            return JsonResponse(
                {"status": 404, "method": "POST", "message": "Topup ID not found"}
            )

        try:
            topup.delete()
            return JsonResponse(
                {
                    "status": 200,
                    "method": "POST",
                    "message": "Topup deleted successfully",
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": 500,
                    "method": "POST",
                    "message": f"Error deleting topup: {str(e)}",
                }
            )
