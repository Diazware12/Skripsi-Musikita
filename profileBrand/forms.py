from django import forms
from product.models import Brand

class AddBrandForm (forms.Form):
    brandName = forms.CharField(
        required=True,
        label='brandName',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Brand Name'
            }
        )
    )

class InviteBrandForm (forms.Form):
    brandName = forms.ModelChoiceField(
        queryset= Brand.objects.filter(status = 'No_User').values_list('brandName', flat=True),
        required=True,
        label="brandName",
        widget=forms.Select(
            attrs={
                'class': 'form-control chosen'
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

    message = forms.CharField(
        required=True,
        label='message',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Type Message'
            }
        )
    )

class registerBrandForm (forms.Form): 

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
    brandWebsiteUrl = forms.CharField(
        required=False,
        label='brandWebsiteUrl',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Brand Website'
            }
        )
    )
    description = forms.CharField(
        required=False,
        label='description',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Brand Description (min. 75 character)'
            }
        )
    )