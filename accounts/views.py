from django.shortcuts import redirect
from django.http import HttpResponse

def login_view(request):
    return redirect("/accounts/github/login/")

def home_view(request):
    return HttpResponse("Copper Rabbit Dashboard")