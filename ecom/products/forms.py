from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['name', 'title', 'message', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review Title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Review'}),
            'rating': forms.HiddenInput(),  # Hidden input for JS
        }

