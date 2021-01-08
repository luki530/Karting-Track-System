from karting_track_system.models import *
from django.http import HttpResponse

def displayRecords(request):
    models = []
    sexes = []
    shapes = []
    no_of_seats = []
    first = True
    query = 'select l.id, l.end_time-l.start_time as "time", t.shape, km.model, c.sex, km.number_of_seats from lap l left join track t on l.track_id=t.id left join race_drivers rd on l.race_drivers_id=rd.id left join kart k on rd.kart_id = k.id left join kart_model km on k.kart_model_id=km.id left join client c on rd.client_id =c.id'
    if request.method=='POST':

        if request.POST.getlist('kart_models'):
            models = request.POST.getlist('kart_models')
            if not first:
                query+=' and '
            else:
                query+=' where '
                first = False
            try:    
                query+='km.id in ('+str(int(models.pop()[0]))
                for model in models:
                    query+=', ' + str(int(model))
            except ValueError:
                print('RAISE EXCEPTION')
            query+=')'

        if request.POST.getlist('sexes'):
            sexes = request.POST.getlist('sexes')
            if not all(len(n) == 1 for n in sexes):
                print('RAISE EXCEPTION')
            if not first:
                query+=' and '
            else:
                query+=' where '
                first = False
            query+='c.sex in (\''+sexes.pop()[0]+'\''
            for sex in sexes:
                query+=', \'' + sex +'\''
            query+=')'

        if request.POST.getlist('tracks'):
            shapes = request.POST.getlist('tracks')
            if not first:
                query+=' and '
            else:
                query+=' where '
                first = False
            try:
                query+='t.id in ('+str(int(shapes.pop()[0]))
                for shape in shapes:
                    query+=', ' + str(int(shape))
            except ValueError:
                print('RAISE EXCEPTION')
            query+=')'

        if request.POST.getlist('seats'):
            no_of_seats = request.POST.getlist('seats')
            if not first:
                query+= ' and '
            else:
                query+=' where '
                first = False
            try:
                query += 'km.number_of_seats in ('+str(no_of_seats.pop()[0])
                for no in no_of_seats:
                    query+=', ' + str(no)
            except ValueError:
                print('RAISE EXCEPTION')
            query+=')'

    query+=' order by time limit 20'
    records = Lap.objects.raw(query)
    return records
