from karting_track_system.models import *
from django.http import HttpResponse

def displayRecords(request):
    models = []
    sexes = []
    shapes = []
    no_of_seats = []
    if request.method=='POST':

        if request.POST.getlist('kart_models'):
            models = request.POST.getlist('kart_models')
            print(models)

        else:
            models = [None]

        if request.POST.getlist('sexes'):
            sexes = request.POST.getlist('sexes')
            print(sexes)
        
        else:
            sexes = [None]

        if request.POST.getlist('tracks'):
            shapes = request.POST.getlist('tracks')
            print(shapes)

        else:
            shapes = [None]

        if request.POST.getlist('seats'):
            no_of_seats = request.POST.getlist('seats')
            print(no_of_seats)

        else:
            no_of_seats = [None]

        records = Lap.objects.raw('select l.id, l.end_time-start_time as "time" , t.shape, km.model, c.sex, km.number_of_seats from lap l natural join track t natural join kart_model km natural join client c where km.id in %s and t.id in %s and km.number_of_seats in %s and c.sex in %s', [tuple(models), tuple(shapes), tuple(no_of_seats), tuple(sexes)])
        print(records)
        return records
    else:
        records = Lap.objects.raw('select l.id, l.end_time-start_time as "time" , t.shape, km.model, c.sex, km.number_of_seats from lap l natural join track t natural join kart_model km natural join client c')      
        return records
