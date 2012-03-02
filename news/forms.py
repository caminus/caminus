from django import forms
import models

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        exclude = ('author', 'post', 'parent', 'created', 'updated')
