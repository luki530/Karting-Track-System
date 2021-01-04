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

        models_placeholders = ', '.join(['{}'] * len(models))
        sexes_placeholders = ', '.join(['\'{}\''] * len(sexes))
        shapes_placeholders = ', '.join(['{}'] * len(shapes))
        no_of_seats_placeholders = ', '.join(['{}'] * len(no_of_seats))
        records = Lap.objects.raw('select l.id, l.end_time-start_time as "time" , t.shape, km.model, c.sex, km.number_of_seats from lap l natural join track t natural join kart_model km natural join client c where km.id in ({}) and t.id in ({}) and km.number_of_seats in ({}) and c.sex in ({})'.format(models_placeholders, shapes_placeholders, no_of_seats_placeholders, sexes_placeholders).format(*models,*shapes,*no_of_seats,*sexes))
        print(records)
        return records
    else:
        records = Lap.objects.raw('select l.id, l.end_time-start_time as "time" , t.shape, km.model, c.sex, km.number_of_seats from lap l natural join track t natural join kart_model km natural join client c')
        return records
