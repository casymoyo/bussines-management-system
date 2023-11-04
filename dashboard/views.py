from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login")
def Dashboard(request):
    return render(request, "dashboard.html")
