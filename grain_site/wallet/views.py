from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify

from .forms import SignUpForm, TopupForm, TransferForm

from .models import Profile, IndividualWallet, Clan, ClanWallet

@login_required
def main(request):
    individual_wallets = IndividualWallet.objects.filter(user=request.user)
    savings = 0.0
    for wallet in individual_wallets:
        savings += wallet.value
    return HttpResponse(render(request, 'wallet/home.html', context={
        'user': request.user,
        'wallets': individual_wallets,
        'savings': savings,
        'clans': request.user.clan_set.all(),
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

@login_required
def wallet(request, wslug):
    individual_wallets = IndividualWallet.objects.filter(user=request.user)
    current_wallet = IndividualWallet.objects.get(user=request.user, slug=wslug)
    if request.method == "POST":
        if 'submit-topup' in request.POST:
            topup = TopupForm(request.POST)
            transfer = TransferForm
            if topup.is_valid():
                current_wallet.value += topup.cleaned_data.get('value')
                current_wallet.save()
            else:
                pass
        elif 'submit-transfer' in request.POST:
            topup = TopupForm
            transfer = TransferForm(request.POST)
            if transfer.is_valid():
                pass
            else:
                pass
    else:
        topup = TopupForm
        transfer = TransferForm
    return HttpResponse(render(request, 'wallet/wallet_page.html', context={
        'user': request.user,
        'wallets': individual_wallets,
        'clans': request.user.clan_set.all(),
        'current_w': current_wallet,
        'topup': topup,
        'transfer': transfer,
    }))

@login_required
def topup(request):
    pass

@login_required
def clan(request, cslug):
    individual_wallets = IndividualWallet.objects.filter(user=request.user)
    current_clan = request.user.clan_set.all().filter(slug=cslug).first()
    clan_wallets = ClanWallet.objects.filter(clan=current_clan)
    return HttpResponse(render(request, 'wallet/clan_page.html', context={
        'user': request.user,
        'wallets': individual_wallets,
        'clans': request.user.clan_set.all(),
        'current_clan': current_clan,
        'clan_wallets': clan_wallets,
    }))

@login_required
def under_construction(request):
    return HttpResponse(render(request, 'wallet/under_construction.html'))
            
