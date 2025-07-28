from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.USER_TYPES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
