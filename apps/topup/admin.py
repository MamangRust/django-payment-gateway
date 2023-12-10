from django.contrib import admin
from .models import Topups
from apps.shared.uniquenumber import unique_order_number


# Register your models here.


class TopupsAdmin(admin.ModelAdmin):
    list_display = ("user", "topup_no", "topup_amount", "topup_method", "topup_time")

    def save_model(self, request, obj, form, change):
        if not obj.topup_no:
            obj.topup_no = unique_order_number()

        super().save_model(request, obj, form, change)


admin.site.register(Topups, TopupsAdmin)
