from django.urls import path
from . import views

app_name = "moviesapp"

urlpatterns = [
    path('',views.demo,name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/add_movie/', views.add_movie, name='add_movie'),
    path('profile/movie/<int:id>/', views.view_movie, name='view_movie'),
    path('profile/edit_movie/<int:id>/', views.edit_movie, name='edit_movie'),
    path('profile/delete_movie/<int:id>/', views.delete_movie, name='delete_movie'),
    path('addreview/<int:id>/', views.add_review, name='add_review'),
    path('search/', views.search_movies, name='search_movies'),

    # path('movie/<int:id>/add_review', views.add_review, name="add_review"),
    # path('movie/<int:movie_id>/add_review/', views.add_review, name='add_review'),
    # path('movie/<int:movie_id>/add_rating/', views.add_rating, name='add_rating'),
    # path('movie/<int:pk>/add_review/', views.add_review, name='add_review'),
    # path('profile/add_review/<int:pk>/', views.add_review, name='add_review'),
    # path('movie/<int:movie_id>/add_review/', views.add_review, name='add_review'),

]
