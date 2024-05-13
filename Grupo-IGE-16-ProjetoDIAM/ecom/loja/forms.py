from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(label='Avaliação', min_value=0, max_value=5)

    class Meta:
        model = Review
        fields = ['rating']


