from karting_track_system.models import *
from karting_track_system.controller import *
from django.http import HttpResponse

def getModels(self):
    models = KartModel.objects.raw('select * from kart_model')
    return models

def getSexes(self):
    sexes = ['M','F']
    return sexes

def getTracks(self):
    tracks = Track.objects.raw('select * from track')
    return tracks

def getSeats(self):
    seats = [1, 2]
    return seats

def getRaces(request):
    races = Race.objects.raw('select * from race r inner join race_drivers rd on r.id=rd.race_id inner join client c on c.id=rd.client_id where c.user_id = %s', [request.user.id])
    return races
#from_unixtime(milliseconds/1000)