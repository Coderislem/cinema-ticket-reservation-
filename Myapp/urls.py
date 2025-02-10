from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('movies_Vset',views.MovieViewSet)
router.register('guest_vset',views.GuestViewSet)
router.register('reservation_Vset',views.ReservationViewSet)

urlpatterns = [
#rest api auth
    path('api-auth/', include('rest_framework.urls')),

    path('movies/', views.noSerializer_noModel,name='movies'),
    path('movies2/', views.noSerializer_withModel,name='movies2'),
    path('movies3/', views.movie_list,name='movies3'),
    path('movies/<int:pk>', views.movie_detail,name='movies-delete'),

    #normal class CBV

    path('movies_class/',views.MovieList.as_view(),name="movies_list"),
    path('movies_class/<int:pk>/',views.MovieDetail.as_view(),name="movies_detail"),
    #mixin class 
    path('movies_mixen/',views.MovieListMixin.as_view(),name="movies_list_mixen"),
    path('movies_mixen/<int:pk>/',views.MovieDetailMixin.as_view(),name="movies_detail_mixen"),
    #generic class 
    path('movies_generic/',views.MovieListGeneric.as_view(),name="movies_list_generic"),
    path('movies_generic/<int:pk>/',views.MovieDetailGeneric.as_view(),name="movies_detail_generic"),
   #ViewSet
    path('',include(router.urls)),
   #search
    path('search/',views.search_movies,name='search_movie'),
    # authtoken
     path('api-token-auth/', obtain_auth_token)
]
