from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from karting_track_system.models import *
from karting_track_system.repository import *
from karting_track_system.controller import *

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from .forms import SignUpForm

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
    return render(request, 'karting_track_system/records.html', {'models': getModels(models), 'sexes': getSexes(sexes), 'tracks': getTracks(tracks), 'seats': getSeats(seats), 'times': displayRecords(request)})


def statistics(request):
    if request.method == 'POST' and 'btn1' in request.POST:
        race_numbers = getDate(request)
        return render(request, 'karting_track_system/statistics.html', {'races': race_numbers})
    elif request.method == 'POST' and 'btn2' in request.POST:

        plots = plot(request)
        full, _ = displayRaces(request)
        return render(request, 'karting_track_system/statistics.html', {'full': full, 'range': range(0, len(full)), 'plots': plots})
    else:
        return render(request, 'karting_track_system/statistics.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html')
    if request.method == 'POST':
        return register(request)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    return activate_user(request, uidb64, token)


def userProfile(request):
    return render(request, 'karting_track_system/userprofile.html')
