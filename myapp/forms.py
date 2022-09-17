from django import forms
from .models import User

class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username']

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        # fields = ['username', 'password'] // If we want to mention selective fields.
        # for all use fields = __all__