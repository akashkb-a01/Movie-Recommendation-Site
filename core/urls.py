from core.views import Home, My_list, ProfileList, ProfileCreate,Watch,ShowMovieDetail, genreList, Recommender
from . import views
from django.urls import path

app_name='core'

urlpatterns = [
    path('movie/detail/<str:profile_id>/<str:movie_id>/',ShowMovieDetail.as_view(),name='show_det'),    
    path('',Home.as_view()),
    path('profile/',ProfileList.as_view(),name='profile_list'),
    path('profile/create/',ProfileCreate.as_view(),name='profile_create'),
    path('watch/<str:profile_id>/',Watch.as_view(),name='watch'),
    path('watch/<str:profile_id>/<str:movie_genre>',genreList.as_view(),name='genre_list'),
    path('recommend/<str:profile_id>/', Recommender.as_view(), name='recommend'),
    path('mylist/<str:profile_id>/', My_list.as_view(), name='mylist'),
]


