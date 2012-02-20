from django import forms
from django.contrib.auth.models import User
import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.MinecraftProfile
        exclude = ('user',)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

class InviteClaimForm(forms.Form):
    code = forms.CharField()
