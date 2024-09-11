from django.contrib import admin
from .models import Movie, Category, Review

# Register your models here.
admin.site.register(Movie)
admin.site.register(Category)
admin.site.register(Review)

