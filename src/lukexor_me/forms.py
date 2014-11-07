from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)


class ContactForm(forms.Form):

    """A simple message form
    """

    name = forms.CharField(
        max_length=45,
        widget=forms.TextInput(
            attrs={
                'class': 'contact_name form-control required',
                'placeholder': 'Name',
            }
        ),
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'contact_email form-control required',
                'placeholder': 'Email',
            }
        ),
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'contact_phone form-control required',
                'placeholder': 'Phone',
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'contact_message form-control required',
                'placeholder': 'Message',
                'rows': 9,
            }
        ),
    )
