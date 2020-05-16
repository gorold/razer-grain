from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

from .models import Profile, Guild

def main(request):
    if request.user.is_authenticated:
        return HttpResponse(render(request, 'wallet/home.html'))
    else:
        return redirect('accounts/login')

def register(request):
    if request.method == "GET":
        form = SignUpForm
        return render(
            request = request,
            template_name = "registration/register.html",
            context = {
                "form": form
                },
        )
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.nric = form.cleaned_data.get('nric')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Congratulations! Your account has been created, please ensure to verify your email.')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(
                request = request,
                template_name = "registration/register.html",
                context = {
                    "form": form
                },
            )
            
