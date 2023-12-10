from django.urls import path
from .views import (
    TopupListView,
    TopupResultView,
    TopupCreateView,
    TopupEditView,
    TopupDeleteView,
)


urlpatterns = [
    path("", TopupListView.as_view(), name="topup-list"),
    path("result/<int:id>", TopupResultView.as_view(), name="topup-result"),
    path("create/", TopupCreateView.as_view(), name="topup-create"),
    path("update/<int:id>", TopupEditView.as_view(), name="topup-edit"),
    path("delete/<int:id>", TopupDeleteView.as_view(), name="topup-delete"),
]
