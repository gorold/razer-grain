from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify
from django.conf import settings

import requests
import json
import base64

from .forms import *
from .models import *

@login_required
def main(request):
    individual_wallets = IndividualWallet.objects.filter(user=request.user)
    savings = 0.0
    for wallet in individual_wallets:
        savings += wallet.value

    new_wallet = NewIndividualWalletForm
    new_clan = NewClanForm
    join_clan = JoinClanForm

    if request.method == "POST":
        
        if "submit-new-wallet" in request.POST:
            new_wallet = NewIndividualWalletForm(request.POST)
            if new_wallet.is_valid():
                # TODO: No repeated names
                wallet_name = new_wallet.cleaned_data.get('name')
                credit_card_number = new_wallet.cleaned_data.get('credit_card_number')
                description = new_wallet.cleaned_data.get('description')
                if description is None or description == "":
                    description = "Add a description for your Wallet!"
                w = IndividualWallet.objects.create(name=wallet_name, user=request.user, value=0, description=description)
                w.save()
                individual_wallets = IndividualWallet.objects.filter(user=request.user)
            else:
                pass

        elif "submit-new-clan" in request.POST:
            new_clan = NewClanForm(request.POST)
            if new_clan.is_valid():
                # TODO: No repeated names
                clan_name = new_clan.cleaned_data.get('name')
                public = new_clan.cleaned_data.get('public')
                description = new_clan.cleaned_data.get('description')
                if description is None or description == "":
                    description = "Add a description for your Clan!"
                c = Clan.objects.create(name=clan_name, public=public, description=description)
                c.save()
                c.members.add(request.user)
                c.save()
            else:
                pass

        elif "submit-join-clan" in request.POST:
            join_clan = JoinClanForm(request.POST)
            if join_clan.is_valid():
                clan_name = join_clan.cleaned_data.get('name')
                c = Clan.objects.get(name=clan_name)
                c.members.add(request.user)
                c.save()
            else:
                pass

    return HttpResponse(render(request, 'wallet/home.html', context={
        'user': request.user,
        'wallets': individual_wallets,
        'clans': request.user.clan_set.all(),
        'savings': savings,
        'new_wallet': new_wallet,
        'new_clan': new_clan,
        'join_clan': join_clan,
    }))

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
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

            # ---------KYC CHECK--------------------
            image = form.cleaned_data.get('nric_image').file
            image_string = base64.b64encode(image.read())
            url = settings.KYC_URL
            payload = {
                "Content-Type": "application/json",
                "x-api-key": settings.KYC_KEY,
                "base64image": image_string.decode('utf-8'),
            }
            resp = requests.post(url=url, data=json.dumps(payload)).json()
            if resp["vision"]["type"] == "No Results":
                user.delete()
                storage = messages.get_messages(request)
                storage.used = True
                messages.error(request, _("Failed to verify NRIC"))
                return render(request, 'registration/register.html', context={
                    'form': form
                })
            #---------------------------------------
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, _('Congratulations! Your account has been created, please ensure to verify your email.'))
            return redirect('/')
        else:
            for msg in form.error_messages:
                messages.error(request, _("Failed to register!"))

    else:
        form = SignUpForm
    return render(request, 'registration/register.html', context={
        'form': form
    })

@login_required
def wallet(request, wslug):
    individual_wallets = IndividualWallet.objects.filter(user=request.user)
    current_wallet = IndividualWallet.objects.get(user=request.user, slug=wslug)

    topup = TopupForm
    transfer = TransferForm
    if request.method == "POST":
        if 'submit-topup' in request.POST:
            topup = TopupForm(request.POST)
            if topup.is_valid():
                current_wallet.value += topup.cleaned_data.get('value')
                current_wallet.save()
            else:
                pass
        elif 'submit-transfer' in request.POST:
            transfer = TransferForm(request.POST)
            if transfer.is_valid():
                pass
            else:
                pass

    return HttpResponse(render(request, 'wallet/wallet_page.html', context={
        'user': request.user,
        'wallets': individual_wallets,
        'clans': request.user.clan_set.all(),
        'current_w': current_wallet,
        'topup': topup,
        'transfer': transfer,
    }))

@login_required
def clan(request, cslug):
    individual_wallets = IndividualWallet.objects.filter(user=request.user)
    current_clan = request.user.clan_set.all().filter(slug=cslug).first()
    clan_wallets = ClanWallet.objects.filter(clan=current_clan)
    
    topup_clan_wallet = ClanWalletTopupForm(request.user)
    withdraw_clan_wallet = ClanWalletWithdrawForm(request.user)
    new_clan_wallet = NewClanWalletForm
    add_member = AddClanMemberForm

    if request.method == "POST":

        if "submit-new-clan-wallet" in request.POST:
            new_clan_wallet = NewClanWalletForm(request.POST)
            if new_clan_wallet.is_valid():
                wallet_name = new_clan_wallet.cleaned_data.get('name')
                have_target = new_clan_wallet.cleaned_data.get('have_target')
                target = new_clan_wallet.cleaned_data.get('target')
                c = ClanWallet.objects.create(clan=current_clan, name=wallet_name, value=0.0, have_target=have_target, target=target)
                c.save()
                ClanWalletAdmin.objects.create(clanwallet=c, user=request.user).save()

            else:
                pass

        if "submit-new-member" in request.POST:
            add_member = AddClanMemberForm(request.POST)
            if add_member.is_valid():
                username = add_member.cleaned_data.get('username')
                member = User.objects.get(username=username)
                current_clan.members.add(member)
                current_clan.save()
            else:
                pass
    
    for cw in clan_wallets:
        if ClanWalletAdmin.objects.filter(clanwallet=cw).filter(user=request.user).exists():
            cw.is_admin = True

    return HttpResponse(render(request, 'wallet/clan_page.html', context={
        'user': request.user,
        'wallets': individual_wallets,
        'clans': request.user.clan_set.all(),
        'current_clan': current_clan,
        'clan_members': current_clan.members.all(),
        'clan_wallets': clan_wallets,
        'add_member': add_member,
        'topup_clan_wallet': topup_clan_wallet,
        'withdraw_clan_wallet': withdraw_clan_wallet,
        'new_clan_wallet': new_clan_wallet,
    }))

@login_required
def clanwallet_topup(request, cslug, cwslug):
    individual_wallets = IndividualWallet.objects.filter(user=request.user)
    current_clan = request.user.clan_set.all().filter(slug=cslug).first()
    clan_wallets = ClanWallet.objects.filter(clan=current_clan)
    current_clan_wallet = clan_wallets.filter(slug=cwslug).first()

    if request.method == "POST":
        topup_clan_wallet = ClanWalletTopupForm(request.user, request.POST)
        if topup_clan_wallet.is_valid():
            my_wallet = topup_clan_wallet.cleaned_data.get('my_wallets')
            amount = topup_clan_wallet.cleaned_data.get('amount')
            iw = individual_wallets.filter(name=my_wallet.name).first()
            if iw.value >= amount:
                iw.value -= amount
                iw.save()
                current_clan_wallet.value += amount
                current_clan_wallet.save()

            else:
                messages.error(request, "Your selected wallet does not have enough funds!")        

    return redirect('/clan/'+cslug)

@login_required
def clanwallet_withdraw(request, cslug, cwslug):
    individual_wallets = IndividualWallet.objects.filter(user=request.user)
    current_clan = request.user.clan_set.all().filter(slug=cslug).first()
    clan_wallets = ClanWallet.objects.filter(clan=current_clan)
    current_clan_wallet = clan_wallets.filter(slug=cwslug).first()

    if request.method == "POST":
        withdraw_clan_wallet = ClanWalletWithdrawForm(request.user, request.POST)
        if withdraw_clan_wallet.is_valid():
            my_wallet = withdraw_clan_wallet.cleaned_data.get('my_wallets')
            amount = withdraw_clan_wallet.cleaned_data.get('amount')
            iw = individual_wallets.filter(name=my_wallet.name).first()
            if current_clan_wallet.value >= amount:
                iw.value += amount
                iw.save()
                current_clan_wallet.value -= amount
                current_clan_wallet.save()

            else:
                pass        

    return redirect('/clan/'+cslug)

@login_required
def under_construction(request):
    return HttpResponse(render(request, 'wallet/under_construction.html'))
            
