from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput(), min_length=5)
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=5)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=5)