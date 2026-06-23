from django.shortcuts import redirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

def login_view(request):
    return redirect("/accounts/github/login/")

@login_required
def home_view(request):
    return render(
        request,
        "dashboard/home.html"
    )