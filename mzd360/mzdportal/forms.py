from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SpecialEvent, Profile

class SpecialEventForm(forms.ModelForm):
    class Meta:
        model = SpecialEvent
        fields = '__all__'

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full bg-transparent p-0 text-sm  text-gray-500 focus:outline-none'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full bg-transparent p-0 text-sm  text-gray-500 focus:outline-none'}),
            'username': forms.TextInput(attrs={'class': 'w-full bg-transparent p-0 text-sm  text-gray-500 focus:outline-none'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-transparent p-0 text-sm  text-gray-500 focus:outline-none'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = Profile
        fields = ['image']



#
