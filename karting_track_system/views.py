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
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]



def home(request):
    return render(request, 'karting_track_system/home.html')

def records(request):
    times = displayRecords(request)
    return render(request, 'karting_track_system/records.html', {'models': getModels(models) ,'sexes':getSexes(sexes), 'tracks': getTracks(tracks), 'seats': getSeats(seats), 'times':displayRecords(request)})

def statistics(request):
    return render(request, 'karting_track_system/statistics.html')

def generateRecords(request):
    return render(request, 'karting_track_system/records.html')