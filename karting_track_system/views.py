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
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
UserModel = get_user_model()

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
    return render(request, 'karting_track_system/records.html', {'models': getModels(models) ,'sexes':getSexes(sexes), 'tracks': getTracks(tracks), 'seats': getSeats(seats), 'times':displayRecords(request)})

def statistics(request):
    if request.method == 'POST' and 'btn1' in request.POST:
        race_numbers = getDate(request)
        return render(request, 'karting_track_system/statistics.html',{'races':race_numbers})
    elif request.method == 'POST' and 'btn2' in request.POST:
        
        plots = plot(request)
        full, _ = displayRaces(request)
        return render(request, 'karting_track_system/statistics.html',{'full': full,'range': range(0,len(full)),'plots':plots})
    else:
        return render(request, 'karting_track_system/statistics.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            #TODO checkforexisting profile
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')