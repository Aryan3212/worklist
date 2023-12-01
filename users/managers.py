from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('email', 'username', 'password1', 'password2')