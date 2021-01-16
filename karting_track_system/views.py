
import json
import requests, random, re
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from karting_track_system.models import *
from karting_track_system.repository import *
from karting_track_system.controller import *

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from datetime import date

from .forms import SignUpForm

from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .bot_logic import LOGIC_RESPONSES

from django.conf import settings
# Create your views here.
models = []
params = []
sexes = []
times = []
tracks = []
seats = []

ongoing_race_id = -1
current_track = 1
ongoing_race = None


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

    elif request.method == 'POST' and 'btn3' in request.POST:

        plots = plot(request)
        full, _ = displayRaces(request)
        return render(request, 'karting_track_system/user_race.html', {'full': full, 'range': range(0, len(full)), 'plots': plots})
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


@login_required
def userProfile(request):
    races = getRaces(request)
    return render(request, 'karting_track_system/userprofile.html', {'races': races})


@staff_member_required
def control_races(request):
    global ongoing_race_id
    global ongoing_race
    global current_track
    tracks = Track.objects.raw('select * from track')

    today = date.today()
    races = Race.objects.raw(
        'select * from race r where r.date=%s', [today])
    if request.method == 'GET':
        if not ongoing_race_id == -1:
            return render(request, 'karting_track_system/control_races.html', {'races': races, 'ongoing_race_id': int(ongoing_race_id), 'tracks' : tracks, 'current_track' : current_track})
        return render(request, 'karting_track_system/control_races.html', {'races': races, 'ongoing_race_id': int(ongoing_race_id), 'tracks' : tracks, 'current_track' : current_track})

    elif request.method == 'POST' and 'btn_start' in request.POST:
        race_id = request.POST.get('races')
        ongoing_race_id = int(race_id)
        return render(request, 'karting_track_system/control_races.html', {'races': races, 'ongoing_race_id': int(ongoing_race_id), 'tracks' : tracks, 'current_track' : current_track})

    elif request.method == 'POST' and 'btn_stop' in request.POST:
        race_id = request.POST.get('races')
        Race.objects.filter(id=race_id).update(finished=1)
        ongoing_race_id = -1
        return render(request, 'karting_track_system/control_races.html', {'races': races, 'ongoing_race_id': int(ongoing_race_id), 'tracks' : tracks, 'current_track' : current_track})
    elif request.method == 'POST' and 'btn3' in request.POST:
        return statistics(request)

@staff_member_required
def change_track(request):
    global current_track
    if request.method == 'POST':
        new_track = request.POST.get('new_track')
        current_track=new_track
        return HttpResponse('gitara')

@csrf_exempt
def insert_lap(request):
    global ongoing_race_id
    global current_track
    if request.method == 'POST':
        kart_id = request.POST.get('kart_id')
        time = request.POST.get('time')
        race_drivers = RaceDrivers.objects.raw(
            'select * from race_drivers rd where rd.kart_id=%s and race_id=%s', [kart_id, ongoing_race_id])
        race_driver = race_drivers[0]
        laps = Lap.objects.raw(
            'select * from lap l where l.race_drivers_id=%s and l.end_time=NULL', [race_driver.id])
        if laps:
            lap = laps[0]
            lap.end_time = time
            Lap.objects.update(lap=lap)
        else:

            Lap.objects.create(
                race_drivers=race_driver, start_time=time, end_time=None, track=current_track, time=None)
        return HttpResponse('gitara siema')
    return HttpResponseBadRequest('cos nie tak')

def policy(request):
    return render(request, 'karting_track_system/policy.html')

VERIFY_TOKEN = settings.VERIFY_TOKEN

FB_ENDPOINT = 'https://graph.facebook.com/v9.0/'

PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN

def parse_and_send_fb_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    msg = None
    for token in tokens:
        if token in LOGIC_RESPONSES:
            msg = random.choice(LOGIC_RESPONSES[token])
            break
        
    if msg is not None:                 
        endpoint = "{FB_ENDPOINT}/me/messages?access_token={PAGE_ACCESS_TOKEN}"
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
        status = requests.post(
            endpoint, 
            headers={"Content-Type": "application/json"},
            data=response_msg)
        print(status.json())
        return stats.json()
    return None
        
        
class FacebookWebhookView(View):
    @method_decorator(csrf_exempt) # required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) #python3.6+ syntax
    
    def get(self, request, *args, **kwargs):
        hub_mode = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != VERIFY_TOKEN:
            print(VERIFY_TOKEN)
            print(hub_token)
            return HttpResponse('Error, invalid token', status=403)
        return HttpResponse(hub_challenge)
            

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    fb_user_id = message['sender']['id'] # sweet!
                    fb_user_txt = message['message'].get('text')
                    if fb_user_txt:
                        parse_and_send_fb_message(fb_user_id, fb_user_txt)
        return HttpResponse("Success", status=200)

