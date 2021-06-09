from django import forms

RADIO_REPORT = [
    ('Offensive Content', 'Offensive Content'),
    ('Content is Copyright', 'Content is Copyright'),
    ('SPAM or Advertising', 'SPAM or Advertising'),
    ('Mature Content', 'Mature Content'),
    ('Distruptive Posting', 'Distruptive Posting'),
    ('Insults of Other User', 'Insults of Other User'),
    ('Illegal Activities', 'Illegal Activities'),
    ('Other Strong Reason', 'Other Strong Reason'),
]

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
                'placeholder':'Review Description (min. 75 character)'
            }
        )
    )

    sellStatus = forms.BooleanField(required=False)

class ReportForm (forms.Form):
    reportReason = forms.ChoiceField(
        choices=RADIO_REPORT,
        widget=forms.RadioSelect(),
        required=True
    )    