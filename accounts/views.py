from django.shortcuts import redirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from reviews.models import Review

def login_view(request):
    return redirect("/accounts/github/login/")

@login_required
def home_view(request):
    reviews = Review.objects.order_by(
        "-created_at"
    )[:5]

    return render(
        request,
        "dashboard/home.html",
        {
            "reviews": reviews
        }
    )