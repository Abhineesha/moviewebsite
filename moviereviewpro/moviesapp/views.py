from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, MovieForm, ReviewForm
from .models import Movie, Review, Category
from .forms import EditProfileForm

# Create your views here.

def demo(request):
    movie = Movie.objects.all()
    context = {
        'movie_list': movie
    }
    return render(request, 'index.html', context)

# Registration View

# Login View
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid credentials")
            return redirect('moviesapp:login')
    return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        first_name1 = request.POST['first_name']
        last_name1 = request.POST['last_name']
        email1 = request.POST['email']
        password1 = request.POST['password']
        cpassword1 = request.POST['password1']
        if password1 == cpassword1:
            if User.objects.filter(username=username1).exists():
                messages.info(request,"Username Taken")
                return redirect('moviesapp:register')
            elif User.objects.filter(email=email1).exists():
                messages.info(request, "Email Taken")
                return redirect('moviesapp:register')
            else:
                user=User.objects.create_user(username=username1,first_name=first_name1,last_name=last_name1,email=email1,password=password1)
                user.save();
                messages.success(request, "Registration successful! Please log in.")
                return redirect('moviesapp:login')
        else:
            messages.info(request,"password not matching")
            return redirect('moviesapp:register')
        return redirect('/')
    return render(request,'register.html')

# User Profile View
@login_required  # Ensures that only logged-in users can access the profile
def profile(request):
    user = request.user  # Get the currently logged-in user
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('moviesapp:profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'editprofile.html', {'form': form})

# Add Movie View
@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('moviesapp:profile')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

#Add movie
def view_movie(request, id):
    movie = get_object_or_404(Movie, pk=id)
    return render(request, 'view_movie.html', {'movie': movie})


# def view_movie(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)  # Fetch the movie by primary key (id)
#     return render(request, 'view_movie.html', {'movie': movie})
#     # reviews = Review.objects.filter(movie=movie).order_by('-created_at')


# Edit Movie View
@login_required
def edit_movie(request, id):
    movie = get_object_or_404(Movie, pk=id, user=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('moviesapp:profile')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form})

# Delete Movie View
# @login_required
# def delete_movie(request, pk):
#     movie = get_object_or_404(Movie, pk=pk, user=request.user)
#     movie.delete()
#     return redirect('profile')
def delete_movie(request, id):
    movie = get_object_or_404(Movie, pk=id)
    # Ensure only the user who added the movie can delete it
    if movie.user != request.user:
        return redirect('moviesapp:profile')  # Or any other page
    if request.method == 'POST':
        movie.delete()
        return redirect('moviesapp:profile')  # Redirect to the profile or movies list
    return render(request, 'delete.html', {'movie': movie})

# Review Movie View
def add_review(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect("moviesapp:add_review", id=movie.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'reviews': reviews})

# def add_review(request, id):
#     if request.user.is_authenticated:
#         movie = Movie.objects.get(id=id)
#         if request.method == "POST":
#             form = ReviewForm(request.POST or None)
#             if form.is_valid():
#                 data = form.save(commit=False)
#                 data.comment = request.POST["comment"]
#                 data.rating = request.POST["rating"]
#                 data.user = request.user
#                 data.movie = movie
#                 data.save()
#                 return redirect("moviesapp:add_review",id)
#         else:
#             form = ReviewForm(request.POST or None)
#             reviews = Review.objects.filter(movie=id)
#         return render(request, 'add_review.html', {"form": form,"reviews":reviews})

# @login_required
# def add_review(request, movie_id):
#     movie = get_object_or_404(Movie,id=movie_id)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.movie = movie
#             review.user = request.user
#             review.save()
#             return redirect('view_movie', movie_id=movie.id)  # Redirect to a movie detail page or wherever you prefer
#     else:
#         form = ReviewForm()
#     return render(request, 'add_review.html', {'form': form, 'movie': movie})
# @login_required
# def add_rating(request, movie_id):
#     movie = get_object_or_404(Movie,id=movie_id)
#     if request.method == 'POST':
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             rating = form.save(commit=False)
#             rating.movie = movie
#             rating.user = request.user
#             rating.save()
#             return redirect('view_movie',movie_id=movie.id)  # Redirect to a movie detail page or wherever you prefer
#     else:
#         form = RatingForm()
#     return render(request, 'add_rating.html', {'form': form, 'movie': movie})

# @login_required
# def review_movie(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.movie = movie
#             review.save()
#             return redirect('movie_detail', pk=movie.pk)
#     else:
#         form = ReviewForm()
#     return render(request, 'review_movie.html', {'form': form, 'movie': movie})

# Movie Detail View
# def movie_detail(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     reviews = movie.reviews.all()
#     return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews})

# Search Functionality
def search_movies(request):
    query = request.GET.get('q')  # Get the search term from the query parameter 'q'
    movies = Movie.objects.filter(title__icontains=query)  # Filter movies by title (case-insensitive)
    return render(request, 'search_results.html', {'movies': movies, 'query': query})
# def search_movies(request):
#     query = request.GET.get('q')
#     movies = Movie.objects.filter(title__icontains=query)
#     return render(request, 'movies/search_results.html', {'movies': movies})

def logout(request):
    auth.logout(request)
    return redirect('/')

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Send Welcome Email
#             send_mail(
#                 'Welcome to MovieReviewPlatform',
#                 'Thank you for registering!',
#                 settings.EMAIL_HOST_USER,
#                 [user.email],
#                 fail_silently=False,
#             )
#             messages.success(request, 'Registration successful.')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'register.html', {'form': form})