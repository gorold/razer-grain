from django.forms import ModelForm, Form, DateInput
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from .models import IndividualWallet

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

# class IndividualWalletForm(ModelForm):

#     class Meta:
#         model = IndividualWallet
#         fields = 