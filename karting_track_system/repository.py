from karting_track_system.models import *
from karting_track_system.controller import *

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



#from_unixtime(milliseconds/1000)