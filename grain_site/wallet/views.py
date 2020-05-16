from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from .forms import SignUpForm

from .models import Profile, IndividualWallet, Guild

@login_required
def main(request):
    individualwallet = IndividualWallet.objects.get(user=request.user)
    return HttpResponse(render(request, 'wallet/home.html', context={
        'user': request.user,
        'wallet': individualwallet,
    }))

def register(request):
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
            user.individualwallet.value = 0
            # -------- Delete: Make admin ----------
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
            # --------------------------------------
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, _('Congratulations! Your account has been created, please ensure to verify your email.'))
            return redirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = SignUpForm
    return render(request, 'registration/register.html', context={
        'form': form
    })

def wallet(request):
    if request.user.is_authenticated:
        return HttpResponse(render(request, 'wallet/wallet_page.html'))
    else:
        return redirect('accounts/login')

def clan(request):
    if request.user.is_authenticated:
        return HttpResponse(render(request, 'wallet/clan_page.html'))
    else:
        return redirect('accounts/login')

def under_construction(request):
    if request.user.is_authenticated:
        return HttpResponse(render(request, 'wallet/under_construction.html'))
    else:
        return redirect('accounts/login')
            
