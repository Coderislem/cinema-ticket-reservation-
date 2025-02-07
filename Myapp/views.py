from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie,Guest,Reservation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieSerializer,GuestSerializer,ReservationSerializer
from rest_framework.views import APIView
from rest_framework.mixins import (ListModelMixin
                                   ,CreateModelMixin
                                   ,RetrieveModelMixin
                                   ,UpdateModelMixin
                                   ,DestroyModelMixin)
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import viewsets

# Create your views here.


def noSerializer_noModel(request):
    movies = [
        {
            'name': 'The Shawshank Redemption',
            'description': 'Two imprisoned  ',
            'rate': 9.3,
            'image': 'https://www.imdb.com/title/tt0111161/mediaviewer/rm10105600/',

            
            },
        {
            'name': 'The Godfather',
            'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
            'rate': 9.2,
            'image': 'https://www.imdb.com/title/tt0068646/mediaviewer/rm10105600/',

            
            },
        {
            'name': 'The Dark Knight',
            'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
            'rate': 9.0,
            'image': 'https://www.imdb.com/title/tt0468569/mediaviewer/rm10105600/',

            
            },
        {
            'name': '12 Angry man',
            'description': 'A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.',
            'rate': 9.0,
            'image': 'https://www.imdb.com/title/tt0050083/mediaviewer/rm10105600/',

            
            },
        
        {
            'name': 'Schindler List',
            'description': 'In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution',
            'rate': 8.9,
            'image': 'https://www.imdb.com/title/tt0108052/mediaviewer/rm10105600/',
        }
    ]
    return JsonResponse(movies,safe=False)
def noSerializer_withModel(request):
    movies = Movie.objects.all()
    respone = [x for x in movies.values('name','description','image')]
    return JsonResponse(respone,safe=False)

#Function based view
#GET and POST
@api_view(['GET','POST'])
def movie_list(request):
    #GET
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

# GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def movie_detail(request,pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=404)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = MovieSerializer(movie,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=204)

#CBV  class based view

# list and create > GET and POST
class MovieList(APIView):
    def get(self,reqeust):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many = True)
        return Response(serializer.data)
    def post(self,request):
        serilazer = MovieSerializer(data = request.data)
        if serilazer.is_valid():
            serilazer.save()
            return Response(serilazer.data,status=201)
        return Response(
            serilazer.errors,
            status=400
        )

#GET PUT DELETE
class MovieDetail(APIView):
    def get_object(self,pk):
        try:
            return Movie.objects.get(pk = pk)
        except Movie.DoesNotExist:
            return Response(status=404)
    def get(self,reqeust,pk):
        movies = self.get_object(pk)
        serializer = MovieSerializer(movies)
        return Response(serializer.data)
    def put(self,request,pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    def delete(self,request,pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=204)

#class mixin
#GET POST
class MovieListMixin(ListModelMixin,CreateModelMixin,GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

#GET PUT DELETE
class MovieDetailMixin(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    def get(self,request,pk):
        return self.retrieve(request)
    def put(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)

# GENERIC VIEW
#GET POST
class MovieListGeneric(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# VIEWSETS
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

#search FBV
from django.db.models import Q  # Used for searching
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer

@api_view(['GET'])
def search_movies(request):
    """Search for movies by name or description."""
    query = request.GET.get('search', '')  # Get search keyword from URL
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(Q(name__icontains=query) | Q(description__icontains=query))

    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



  