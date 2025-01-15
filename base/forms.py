from django.forms import ModelForm
from.models import Room
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username','email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'Username is required.',
                'invalid': 'Enter a valid username.',
            },
            'password1': {
                'required': 'Password is required.',
                'invalid': 'Enter a strong password.',
            },
            'password2': {
                'required': 'Password confirmation is required.',
                'invalid': 'Passwords do not match.',
            },
        }