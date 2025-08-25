from django.shortcuts import render, redirect, HttpResponse
from users.forms import CustomRegistrationForm, CustomLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator

def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False  # User is inactive until they activate their account
            user.save()

            # form.save()
            messages.success(request, 'Registration successful!')            
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, 'registration/signup.html', {"form": form})

def sign_in(request):
    form = CustomLoginForm()    
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("User logged in successfully", user)
            return redirect('home')
    return render(request, 'registration/login.html', {"form": form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def activate_user(request, user_id, token):    
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('sign-in')
        else:
            return HttpResponse("Activation link is invalid or has expired.")
    except User.DoesNotExist:
        return HttpResponse("User does not exist")
