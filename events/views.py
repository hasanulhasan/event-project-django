from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def details(request):
    return render(request, "details.html")

def dashboard(request):
    return render(request, "dashboard.html")