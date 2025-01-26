from django.contrib.auth.forms import UserCreationForm , UserChangeForm

from django.contrib.auth import get_user_model
from .models import CustomUser

from django import forms 
from .models import GetToken, Hesabha

class CustomCreationForm(UserCreationForm):
    class Meta:
        model= CustomUser
        fields = ('username' , 'email' ,'lisence' ,)


class CustomChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username' , 'email' , 'lisence' , )
    

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput , max_length=255)

class CheckToken (forms.ModelForm):
    TOKEN =  forms.CharField(max_length=200 , required=False)
    class Meta:
        model = GetToken
        fields = ('TOKEN',)


class AddHesab (forms.Form):
    code_hesab =  forms.CharField(max_length=200)
    name_hesab =  forms.CharField(max_length=200 )


class GatherMoein (forms.Form):
    token = forms.CharField(max_length=200)
    hesab_id = forms.CharField(max_length=200)