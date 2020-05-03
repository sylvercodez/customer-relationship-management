from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class account_settingsform(ModelForm):
    class Meta():
        model = Customers
        fields = '__all__'
        exclude = ['user']

class createform_Order(ModelForm):
    class Meta():
        model = Orders
        fields = '__all__'


class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] 