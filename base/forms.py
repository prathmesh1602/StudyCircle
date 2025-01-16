from django.forms import ModelForm
from.models import Room,User, UserDetails

from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['college_name', 'department_name', 'current_year', 'linkedin_url', 'github_url', 'twitter_url', 'other_links']
        
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