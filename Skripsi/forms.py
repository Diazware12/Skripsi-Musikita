from django import forms

class LoginForm (forms.Form):
    userEmail = forms.EmailField(
        required=True,
        label='userEmail',
        widget=forms.EmailInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    userPassword = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control'
            }
        ),
        label='userPassword',
    )
