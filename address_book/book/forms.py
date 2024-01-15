"""
    Module name :- forms
    Classes :- UserForm, LoginForm
"""

from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    """
    Form for User Registration.
    """

    class Meta:
        """
        Meta class for user registration form.
        """

        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    """
    Form for User Login
    """

    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    username.widget.attrs.update({"class": "form-control"})
    password.widget.attrs.update({"class": "form-control"})
