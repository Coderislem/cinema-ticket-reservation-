from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieSerializer
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
    

