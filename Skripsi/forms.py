from django import forms

class ForgotPasswordForm (forms.Form):
    userPassword = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'new password'
            }
        ),
        label='userPassword',
    )

    confUserPassword = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'confirm password'
            }
        ),
        label='confUserPassword',
    )
