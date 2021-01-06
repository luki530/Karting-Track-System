from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from karting_track_system.models import *
from karting_track_system.repository import *
from karting_track_system.controller import *
# Create your views here.
models = []
params = []
sexes = []
times = []
tracks = []
seats = []



def home(request):
    return render(request, 'karting_track_system/home.html')

def records(request):
    times = displayRecords(request)
    return render(request, 'karting_track_system/records.html', {'models': getModels(models) ,'sexes':getSexes(sexes), 'tracks': getTracks(tracks), 'seats': getSeats(seats), 'times':displayRecords(request)})

def statistics(request):
    race_numbers = getDate(request)
    if request.method == 'POST':
        return render(request, 'karting_track_system/races.html',{'races':race_numbers})
    else:
        return render(request, 'karting_track_system/statistics.html')

def races(request):
    full = displayRaces(request)
    graph = return_graph(request)
    return render(request, 'karting_track_system/races.html',{'full': full,'range': range(0,len(full)), 'graph':graph})
    
   

