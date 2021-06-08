from django import forms

class CarouselForm (forms.Form):
    imageActive = forms.BooleanField(required=False)

    carouselPicture = forms.ImageField(
        label='carouselPicture',
    )
