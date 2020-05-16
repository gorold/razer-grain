from django.forms import ModelForm, Form, DateInput
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from .models import IndividualWallet, Clan, ClanWallet

from django.core.validators import RegexValidator
numerals = RegexValidator(r'^[0-9]*$', 'Only alphanumeric characters are allowed.')

# from .models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    nric = forms.CharField(max_length=9, required=True)
    country = CountryField().formfield(required=True)
    date_of_birth = forms.DateField(widget=DateInput(attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}), required=True)    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'nric', 'country', 'date_of_birth']

class NewIndividualWalletForm(ModelForm):
    credit_card_number = forms.CharField(label='Credit Card Number', max_length=16, validators=[numerals], required=True)
    class Meta:
        model = IndividualWallet
        fields = ['name', 'credit_card_number']

class NewClanForm(ModelForm):
    class Meta:
        model = Clan
        fields = ['name', 'public']

class JoinClanForm(Form):
    name = forms.CharField(max_length=200, required=True)

class TopupForm(Form):
    value = forms.FloatField(min_value=0)


    class Meta:
        widgets = {
            'topup_value': forms.NumberInput()
        }

class TransferForm(Form):
    value = forms.FloatField(min_value=0)
    to_account = forms.CharField(label='Account', max_length=200, required=True)
    class Meta:
        widgets = {
            'topup_value': forms.NumberInput()
        }

class NewClanWalletForm(ModelForm):
    class Meta:
        model = ClanWallet
        fields = ['name']