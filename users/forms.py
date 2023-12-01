# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import EmailField
from .models import User

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email")

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "email")