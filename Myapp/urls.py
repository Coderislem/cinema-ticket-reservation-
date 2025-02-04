from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('movies',views.MovieViewSet)

urlpatterns = [
    path('movies/', views.noSerializer_noModel,name='movies'),
    path('movies2/', views.noSerializer_withModel,name='movies2'),
    path('movies3/', views.movie_list,name='movies3'),
    path('movies/<int:pk>', views.movie_detail,name='movies-delete'),
    path('movies_class/',views.MovieList.as_view(),name="movies_list"),
    path('movies_class/<int:pk>/',views.MovieDetail.as_view(),name="movies_detail"),
    path('movies_mixen/',views.MovieListMixin.as_view(),name="movies_list_mixen"),
    path('movies_mixen/<int:pk>/',views.MovieDetailMixin.as_view(),name="movies_detail_mixen"),
    path('movies_generic/',views.MovieListGeneric.as_view(),name="movies_list_generic"),
    path('movies_generic/<int:pk>/',views.MovieDetailGeneric.as_view(),name="movies_detail_generic"),
    path('movies_viewset/',include(router.urls)),
]
