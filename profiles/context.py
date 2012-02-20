import models
import forms

def random_quote(request):
    quote = models.Quote.objects.order_by('?')
    if len(quote) > 0:
        return {'quote': quote[0]}
    return {}

def login_form(request):
    return {'login_form': forms.LoginForm()}
