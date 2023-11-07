from myadmin.models import *
from django import forms
class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField()
    empcode = forms.CharField(max_length=10)
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

