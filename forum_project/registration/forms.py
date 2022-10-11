from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    city = forms.CharField(max_length=30)
    profession = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'city', 'profession', 'password1', 'password2', )

