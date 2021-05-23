from django import forms

class ReviewForm (forms.Form):
    reviewTitle = forms.CharField(
        required=True,
        label='reviewTitle',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Title For Review'
            }
        )
    )

    reviewDescription = forms.CharField(
        required=True,
        label='reviewDescription',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Review Description'
            }
        )
    )