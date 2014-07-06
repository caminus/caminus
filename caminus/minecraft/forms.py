from django import forms
from django.contrib.auth.models import User
import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.MinecraftProfile
        exclude = ('user',)

