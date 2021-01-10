from karting_track_system.models import *
from django.http import HttpResponse
from collections import OrderedDict
from plotly.offline import plot, iplot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
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
    full_for_plot = []
    temp_lent = 0

    if request.method == 'POST':
        if request.POST.getlist('races'):
            numbers = request.POST.getlist('races')
            # print(numbers)
        drivers = RaceDrivers.objects.raw('select * from race_drivers rd left join race r on rd.race_id=r.id where r.id = %s', [numbers])

        for rd in drivers:
            times = Lap.objects.raw('select l.id, l.end_time-l.start_time as "time" from lap l left join race_drivers rd on l.race_drivers_id=rd.id left join client c on rd.client_id=c.id where l.race_drivers_id = %s order by l.id',[rd.id])
            race_info = RaceDrivers.objects.raw('select rd.id, avg(l.end_time-l.start_time) as "mean", max(l.end_time-l.start_time) as "worst", min(l.end_time-l.start_time) as "best", c.name from race_drivers rd left join lap l on l.race_drivers_id=rd.id left join client c on rd.client_id=c.id where l.race_drivers_id = %s group by rd.id',[rd.id])
            
            if len(times) > temp_lent:
                temp_lent = len(times)
            
            base = [race_info[0].name, race_info[0].best, race_info[0].worst, round(race_info[0].mean)]

            for i in range(1,len(base)):
                base[i] = datetime.datetime.fromtimestamp(base[i]/1000).strftime('%M:%S.%f')[:-3]

            x = [datetime.datetime.fromtimestamp(i.time/1000).strftime('%M:%S.%f')[:-3] for i in times]
            full.append(base + x)



            x_for_plot = [i.time for i in times]
            full_for_plot.append([race_info[0].name, race_info[0].best, race_info[0].worst, race_info[0].mean] + x_for_plot)
        
        lent = ['#' + str(i) for i in range(1, temp_lent+1)]
        first_col = ['Name','Best time','Worst time','Mean time'] + lent
        full.insert(0,first_col)
        full_for_plot.insert(0,first_col)
        # for i in range(1,len(full)):
        #     print(full[i][4:-1])

        return full, full_for_plot



def displayRecords(request):
    models = []
    sexes = []
    shapes = []
    no_of_seats = []
    cos = '123Michal13'
    if request.method=='POST':

        if request.POST.getlist('kart_models'):
            models = request.POST.getlist('kart_models')
            # print(models)
            # print(int(cos))

        else:
            models = [None]

        if request.POST.getlist('sexes'):
            sexes = request.POST.getlist('sexes')
            # print(sexes)
        
        else:
            sexes = [None]

        if request.POST.getlist('tracks'):
            shapes = request.POST.getlist('tracks')
            # print(shapes)

        else:
            shapes = [None]

        if request.POST.getlist('seats'):
            no_of_seats = request.POST.getlist('seats')
            # print(no_of_seats)

        else:
            no_of_seats = [None]

        models_placeholders = ', '.join(['{}'] * len(models))
        sexes_placeholders = ', '.join(['\'{}\''] * len(sexes))
        shapes_placeholders = ', '.join(['{}'] * len(shapes))
        no_of_seats_placeholders = ', '.join(['{}'] * len(no_of_seats))
        records = Lap.objects.raw('select l.id, l.end_time-l.start_time as "time", t.shape, km.model, c.sex, km.number_of_seats from lap l left join track t on l.track_id=t.id left join race_drivers rd on l.race_drivers_id=rd.id left join kart k on rd.kart_id = k.id left join kart_model km on k.kart_model_id=km.id left join client c on rd.client_id =c.id where km.id in ({}) and t.id in ({}) and km.number_of_seats in ({}) and c.sex in ({})'.format(models_placeholders, shapes_placeholders, no_of_seats_placeholders, sexes_placeholders).format(*models,*shapes,*no_of_seats,*sexes))
        for i in range(0,len(records)):
            records[i].time = datetime.datetime.fromtimestamp(records[i].time/1000).strftime('%M:%S.%f')[:-3]
        return records
    else:
        records = Lap.objects.raw('select l.id, l.end_time-l.start_time as "time", t.shape, km.model, c.sex, km.number_of_seats from lap l left join track t on l.track_id=t.id left join race_drivers rd on l.race_drivers_id=rd.id left join kart k on rd.kart_id = k.id left join kart_model km on k.kart_model_id=km.id left join client c on rd.client_id =c.id limit 20')
        for i in range(0,len(records)):
            records[i].time = datetime.datetime.fromtimestamp(records[i].time/1000).strftime('%M:%S.%f')[:-3]
        return records



def plot(request):
    y = []
    x = []
    title = []
    _, axis = displayRaces(request)
    for i in range(1,len(axis)):
        y.append(axis[i][4:])
        x.append([i for i in range(1, len(y[i-1])+1)])
        title.append(axis[i][0])

    # print(x)
    # print(y)
    # print(title)
    fig = make_subplots(x_title='Lap number',y_title='Time in milliseconds')
    colors=["#800000", "#FF0000", "#800080", "#FF00FF","#008000", "#00FF00", "#808000","#000080", "#0000FF", "#008080", "#00FFFF"]
    for i in range(0,len(title)):
        fig.add_trace(go.Scatter(x=x[i], y=y[i],mode='lines', name=title[i],opacity=0.8, marker_color=colors[i]))
  
    # updatemenus=list([
    # dict(
    #     buttons=[],
    #     direction = 'down',
    #     pad = {'r': 10, 't': 10},
    #     showactive = True,
    #     x = 0,
    #     xanchor = 'left',
    #     y = 1.2,
    #     yanchor = 'top' 
    #     ),
    # ])

    # lister = []
    # for k in range(0,len(title)):
    #     lister.append(dict(
    #         args=['visible', [True for k in range(0,len(title))] if k == 0 else [True if (i+1) == k else False for i in range(0,len(title))]],
    #         label=str( 'All' if k == 0 else title[k]),
    #         method='restyle'
    #     ))

    # updatemenus[0]['buttons'] = lister

    # fig['layout']['updatemenus'] = updatemenus

    return fig.to_html(full_html=False, include_plotlyjs='cdn',default_height=800, default_width = 1200)