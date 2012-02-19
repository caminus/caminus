from django import forms
import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.MinecraftProfile
        exclude = ('user',)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
