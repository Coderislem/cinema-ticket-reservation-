from django.urls import path
from . import views
urlpatterns = [
    path('movies/', views.noSerializer_noModel,name='movies'),
    path('movies2/', views.noSerializer_withModel,name='movies2'),
    path('movies3/', views.movie_list,name='movies3'),
]
