from django.urls import path
from .views import (
    TransferResultsView,
    TransferResultView,
    TransferCreateView,
    TransferEditView,
    TransferDeleteView,
)


urlpatterns = [
    path("", TransferResultsView.as_view(), name="transfer-list"),
    path("result/<int:id>", TransferResultView.as_view(), name="transfer-result"),
    path("create/", TransferCreateView.as_view(), name="transfer-create"),
    path("update/<int:id>", TransferEditView.as_view(), name="transfer-edit"),
    path("delete/<int:id>", TransferDeleteView.as_view(), name="transfer-delete"),
]
