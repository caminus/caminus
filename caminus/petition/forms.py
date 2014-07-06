from django import forms
import models

class PetitionForm(forms.ModelForm):
    class Meta:
        model = models.Petition
        exclude = ('author', 'created', 'updated', 'closed')

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        exclude = ('author', 'created', 'updated', 'petition')
