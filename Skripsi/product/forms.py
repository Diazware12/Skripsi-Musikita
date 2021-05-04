from django import forms
from .models import Product
from embed_video.fields import EmbedVideoField

class ProductForm (forms.Form):
    productName = forms.CharField(
        required=True,
        label='ProductName',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Product Name'
            }
        )
    )

    description = forms.CharField(
        required=True,
        label='Description',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Product Description'
            }
        )
    )

    videoUrl = forms.CharField(
        required=True,
        label='VideoUrl',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Video Link'
            }
        )
    )