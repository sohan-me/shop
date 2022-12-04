from django import forms
from .models import ReviewRating

class ReviewRatingForm(forms.ModelForm):

	class Meta:
		
		model = ReviewRating
		fields = ['rating', 'review']