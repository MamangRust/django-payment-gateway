from django.urls import path
from .views import (
    SaldoListView,
    SaldoResultView,
    SaldoCreateView,
    SaldoEditView,
    SaldoDeleteView,
)

urlpatterns = [
    path("", SaldoListView.as_view(), name="saldo-list"),
    path("result/<int:id>", SaldoResultView.as_view(), name="saldo-result"),
    path("create/", SaldoCreateView.as_view(), name="saldo-create"),
    path("update/<int:id>", SaldoEditView.as_view(), name="saldo-edit"),
    path("delete/<int:id>", SaldoDeleteView.as_view(), name="saldo-delete"),
]
