from django import forms
from .models import Product
from embed_video.fields import EmbedVideoField
from product.models import Category, SubCategory, Brand

class ProductForm (forms.Form):
    productName = forms.CharField(
        required=True,
        label='productName',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Product Name'
            }
        )
    )


    productBrand = forms.ModelChoiceField(
        queryset=Brand.objects.values_list('brandName', flat=True).order_by('brandName'),
        required=True,
        label="brandName",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    description = forms.CharField(
        required=True,
        label='description',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Product Description (min. 75 character)'
            }
        )
    )

    videoUrl = forms.CharField(
        required=True,
        label='videoUrl',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Video Link'
            }
        )
    )

    productPicture = forms.ImageField(
        required=True,
        label='productPicture',
    )

class EditorForm (forms.Form):
    imageActive = forms.BooleanField(required=False)