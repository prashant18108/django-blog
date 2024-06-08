from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model = User
        fields = ("email","username","password1", "password2")