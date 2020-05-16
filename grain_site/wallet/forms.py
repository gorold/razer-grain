from django.forms import ModelForm, Form, DateInput
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from .models import IndividualWallet

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

class NewWalletForm(Form):
    name = forms.CharField(label='Name of new wallet', max_length=200, required=True)
    credit_card_number = forms.CharField(label='Credit Card Number', max_length=16, validators=[numerals], required=True)

class TransactionForm(Form):
    topup_value = forms.FloatField(min_value=0)

    class Meta:
        widgets = {
            'topup_value': forms.NumberInput()
        }
