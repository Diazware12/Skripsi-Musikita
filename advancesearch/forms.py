from django import forms
from product.models import Product
from embed_video.fields import EmbedVideoField
from product.models import Category, SubCategory, Brand

SORT = [
    ('', 'Sort By'),
    ('-dtm_crt', 'Latest Release'),
    ('-avgScore', 'Rating')
]

class ProductFilterForm (forms.Form):
    productName = forms.CharField(
        required=False,
        label='productName',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Product Name'
            }
        )
    )

    sort = forms.ChoiceField(
        choices = SORT,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )


    productBrand = forms.ModelChoiceField(
        queryset=Brand.objects.values_list('brandName', flat=True),
        required=False,
        label="brandName",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )