from django.urls import path
from .views import (
    WithdrawListView,
    WithdrawResultView,
    WithdrawCreateView,
    WithdrawEditView,
    WithdrawDeleteView,
)

urlpatterns = [
    path("", WithdrawListView.as_view(), name="withdraw-list"),
    path("result/<int:id>", WithdrawResultView.as_view(), name="withdraw-result"),
    path("create/", WithdrawCreateView.as_view(), name="withdraw-create"),
    path("update/<int:id>", WithdrawEditView.as_view(), name="withdraw-edit"),
    path("delete/<int:id>", WithdrawDeleteView.as_view(), name="withdraw-delete"),
]
