from django.urls import path

from .views import review_detail

urlpatterns = [
    path(
        "<int:review_id>/",
        review_detail,
        name="review_detail"
    ),
]