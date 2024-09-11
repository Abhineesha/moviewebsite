from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
# Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.TextField()
    trailer_link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
# Review Model
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=100000)
    rating = models.FloatField(default=0)
    def __str__(self):
        return self.user.username
        # return f"{self.user} reviewed {self.movie} rated {self.movie} as {self.rating}"


# class Review(models.Model):
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     review_text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.user} reviewed {self.movie}"
# # Rating Model
# class Rating(models.Model):
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField()
#     def __str__(self):
#         return f"{self.user} rated {self.movie} as {self.rating}"

