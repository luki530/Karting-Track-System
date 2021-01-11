from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
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
    return render(request, 'karting_track_system/records.html', {'models': getModels(models) ,'sexes':getSexes(sexes), 'tracks': getTracks(tracks), 'seats': getSeats(seats), 'times':displayRecords(request)})

def statistics(request):
    if request.method == 'POST' and 'btn1' in request.POST:
        race_numbers = getDate(request)
        request.session['date'] = str(race_numbers)
        return render(request, 'karting_track_system/statistics.html',{'races':race_numbers})
    elif request.method == 'POST' and 'btn2' in request.POST:
        
        plots = plot(request)
        full, _ = displayRaces(request)
        return render(request, 'karting_track_system/statistics.html',{'full': full,'range': range(0,len(full)),'plots':plots})
    else:
        return render(request, 'karting_track_system/statistics.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'karting_track_system/signup.html', {'form': form})

# def races(request):
#     full = displayRaces(request)
#     return render(request, 'karting_track_system/races.html',{'full': full,'range': range(0,len(full))})
    
   

