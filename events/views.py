from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    # return HttpResponse("<h1 style='color: red'>This is contact page</h1>")
    return render(request, "home.html")