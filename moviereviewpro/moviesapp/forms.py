from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Review
# User Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

# Movie Form
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'trailer_link', 'category']

# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment", "rating"]
        labels = {
            'comment': '',
            'rating': '',
            }
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rating'})
            }

# class RatingForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['rating']
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
