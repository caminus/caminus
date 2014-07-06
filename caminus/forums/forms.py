from django import forms
import models

class ReplyForm(forms.ModelForm):
    class Meta:
        model = models.Post
        exclude = ('user', 'parent')

class TopicForm(forms.ModelForm):
    class Meta:
        model = models.Topic
        exclude = ('forum', 'rootPost', 'sticky')
