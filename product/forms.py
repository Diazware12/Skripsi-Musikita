from django import forms
from .models import Product
from embed_video.fields import EmbedVideoField
from product.models import Category, SubCategory, Brand

# FAVORITE_COLORS_CHOICES = [
#     ('blue', 'Blue'),
#     ('green', 'Green'),
#     ('black', 'Black'),
# ]

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
        queryset=Brand.objects.values_list('brandName', flat=True),
        required=True,
        label="brandName",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    # category = forms.ModelChoiceField(
    #     queryset=Category.objects.values(),
    #     label="categoryName"
    # )
    
    # subCategory = forms.ModelChoiceField(
    #     queryset=SubCategory.objects.values_list('subCategoryName', flat=True),
    #     label="categoryName"
    # )
    
    # category = forms.ChoiceField(
    #     choices=FAVORITE_COLORS_CHOICES
    # )

    # subCategory = forms.ChoiceField(
    #     choices=FAVORITE_COLORS_CHOICES
    # )

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