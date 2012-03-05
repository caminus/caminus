import forms

def login_form(request):
    return {'login_form': forms.LoginForm()}
