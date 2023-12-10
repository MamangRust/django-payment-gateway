from django.shortcuts import render
from apps.topup.models import Topups
from apps.saldo.models import Saldo
from apps.transfer.models import Transfer
from apps.withdraw.models import Withdraw
from django.views import View
from django.http import JsonResponse
import json
from django.db.models import Sum, Count
from collections import Counter
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    redirect_field_name = "/auth/login/"

    def get(self, request):
        try:
            user_count = Saldo.objects.values("user").distinct().count()
            topup_count = Topups.objects.count()

            transfer_count = Transfer.objects.count()
            withdraw_count = Withdraw.objects.count()
            topup_method_usage = self.get_topup_method_usage()
            yearly_revenue = self.calculate_yearly_revenue()
            total_topup_amount = Topups.objects.aggregate(
                total_topup=Sum("topup_amount")
            )["total_topup"]

            response_data = {
                "saldo_user_count": user_count,
                "topups_count": topup_count,
                "transfer_count": transfer_count,
                "withdraw_count": withdraw_count,
                "yearly_revenue": yearly_revenue,
                "total_topup_amount": total_topup_amount,
                "topup_method_usage": topup_method_usage,
            }

            return render(
                request=request,
                template_name="admin/dashboard.html",
                context=response_data,
            )

        except Exception as err:
            return JsonResponse({"error": str(err)}, status=400)

    def calculate_yearly_revenue(self):
        yearly_revenue = []
        for month in range(1, 13):
            total_revenue = (
                Topups.objects.filter(created_at__month=month).aggregate(
                    total_revenue=Sum("topup_amount")
                )["total_revenue"]
                or 0
            )
            yearly_revenue.append(total_revenue)
        return yearly_revenue

    def get_topup_method_usage(self):
        topup_method_counts = (
            Topups.objects.values("topup_method")
            .annotate(count=Count("topup_method"))
            .order_by("-count")
        )

        topup_method_dict = {}
        for entry in topup_method_counts:
            topup_method_dict[entry["topup_method"]] = entry["count"]

        return json.dumps(topup_method_dict)
