from karting_track_system.models import *
from django.http import HttpResponse
from collections import OrderedDict
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np

def getDate(request):
    date = []
    if request.method=='POST':
        if request.POST.getlist('date'):
            date = request.POST.getlist('date')
            print(date)

        dates = Race.objects.raw('select id, date, number from race where date = %s', tuple(date))
        print(dates)
        return dates
        
def displayRaces(request):
    numbers = []
    laps = []
    full = []
    temp_lent = 0
    if request.method == 'POST':
        if request.POST.getlist('races'):
            numbers = request.POST.getlist('races')
            print(numbers)
        drivers = RaceDrivers.objects.raw('select * from race_drivers rd left join race r on rd.race_id=r.id where r.id = %s', [numbers])

        for rd in drivers:
            times = Lap.objects.raw('select l.id, l.end_time-l.start_time as "time" from lap l left join race_drivers rd on l.race_drivers_id=rd.id left join client c on rd.client_id=c.id where l.race_drivers_id = %s order by l.id',[rd.id])
            race_info = RaceDrivers.objects.raw('select rd.id, avg(l.end_time-l.start_time) as "mean", max(l.end_time-l.start_time) as "worst", min(l.end_time-l.start_time) as "best", c.name from race_drivers rd left join lap l on l.race_drivers_id=rd.id left join client c on rd.client_id=c.id where l.race_drivers_id = %s group by rd.id',[rd.id])
            
            if len(times) > temp_lent:
                temp_lent = len(times)

            x = [i.time for i in times]
            full.append([race_info[0].name, race_info[0].best, race_info[0].worst, race_info[0].mean] + x)
        
        lent = ['#' + str(i) for i in range(1, temp_lent+1)]
        first_col = ['Name','Best time','Worst time','Mean time'] + lent
        full.insert(0,first_col)
        print(full[1][4:-1])

        return full

def return_graph(request):
    axis = displayRaces(request)
    y = axis[1][4:-1]
    x = [j for j in range(1,len(y)+1)]
    
    

    fig = plt.figure()
    plt.plot(x,y)

    plt.title(str(axis[1][0]) + " - times of laps")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def displayRecords(request):
    models = []
    sexes = []
    shapes = []
    no_of_seats = []
    cos = '123Michal13'
    if request.method=='POST':

        if request.POST.getlist('kart_models'):
            models = request.POST.getlist('kart_models')
            print(models)
            print(int(cos))

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
        records = Lap.objects.raw('select l.id, l.end_time-l.start_time as "time", t.shape, km.model, c.sex, km.number_of_seats from lap l left join track t on l.track_id=t.id left join race_drivers rd on l.race_drivers_id=rd.id left join kart k on rd.kart_id = k.id left join kart_model km on k.kart_model_id=km.id left join client c on rd.client_id =c.id where km.id in ({}) and t.id in ({}) and km.number_of_seats in ({}) and c.sex in ({})'.format(models_placeholders, shapes_placeholders, no_of_seats_placeholders, sexes_placeholders).format(*models,*shapes,*no_of_seats,*sexes))
        print(records)
        return records
    else:
        records = Lap.objects.raw('select l.id, l.end_time-l.start_time as "time", t.shape, km.model, c.sex, km.number_of_seats from lap l left join track t on l.track_id=t.id left join race_drivers rd on l.race_drivers_id=rd.id left join kart k on rd.kart_id = k.id left join kart_model km on k.kart_model_id=km.id left join client c on rd.client_id =c.id limit 20')
        return records