from django import forms
from .models import User

USER_OCCASION = [
    ('Beginner', 'Beginner'),
    ('Musician', 'Musician'),
    ('Music Journalist', 'Music Journalist'),
    ('Sound Engineer', 'Sound Engineer'),
    ('Music Producer', 'Music Producer'),
]

class UserForm (forms.Form):

    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Username (Max. 20 Character)'
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

    occasion = forms.ChoiceField(
        choices=USER_OCCASION,
        widget=forms.RadioSelect(),
        required=True
    )
    
class MusicStoreForm (forms.Form):

    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Music Store Name (Max. 20 Character)'
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
                'placeholder':'Email (Max. 60 Character)'
            }
        )
    )

    contact = forms.CharField(
        required=True,
        label='contact',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Music Store Phone Contact (numeric)'
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

    musicStorePicture2 = forms.ImageField(
        required=True,
        label='musicStorePicture2',
    )

    musicStorePicture3 = forms.ImageField(
        required=True,
        label='musicStorePicture3',
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

class RejectionReason (forms.Form):       
    
    reason = forms.CharField(
        required=True,
        label='Rejection Reason',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Reason for Rejection'
            }
        )
    ) 

class DeleteReason (forms.Form):       
    
    reason = forms.CharField(
        required=True,
        label='Delete Reason',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Reason for Deletion'
            }
        )
    ) 

class resetPassword (forms.Form):       
    
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