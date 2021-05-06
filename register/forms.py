from django import forms
from .models import User

class UserForm (forms.Form):

    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Username'
            }
        )
    )
    
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Email'
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Password'
            }
        ),
        label='Password',
    )
    
    confirm_pass= forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Confirm Password'
            }
        ),
        label='confirm_pass',
    )
    
class MusicStoreForm (forms.Form):

    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Music Store Name'
            }
        )
    )
    
    address = forms.CharField(
        required=True,
        label='Address',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Music Store Address'
            }
        )
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Email'
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Password'
            }
        ),
        label='Password',
    )

    confirm_pass= forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Confirm Password'
            }
        ),
        label='confirm_pass',
    )

    musicStorePicture = forms.ImageField(
        required=True,
        label='musicStorePicture',
    )

    description = forms.CharField(
        required=True,
        label='description',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Description'
            }
        )
    )
        