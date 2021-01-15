from karting_track_system.models import *
from django.http import HttpResponse, HttpResponseBadRequest
from collections import OrderedDict
from plotly.offline import plot, iplot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from .forms import SignUpForm

UserModel = get_user_model()


def displayRecords(request):
    models = []
    sexes = []
    shapes = []
    no_of_seats = []

    first = True
    query = 'select l.id, l.end_time-l.start_time as "time", t.shape, km.model, c.sex, km.number_of_seats, c.name from lap l left join track t on l.track_id=t.id left join race_drivers rd on l.race_drivers_id=rd.id left join kart k on rd.kart_id = k.id left join kart_model km on k.kart_model_id=km.id left join client c on rd.client_id = c.id'

    if request.method == 'POST':

        if request.POST.getlist('kart_models'):
            models = request.POST.getlist('kart_models')
            if not first:
                query += ' and '
            else:
                query += ' where '
                first = False
            try:
                query += 'km.id in ('+str(int(models.pop()[0]))
                for model in models:
                    query += ', ' + str(int(model))
            except ValueError:
                print('RAISE EXCEPTION')
            query += ')'

        if request.POST.getlist('sexes'):
            sexes = request.POST.getlist('sexes')
            if not all(len(n) == 1 for n in sexes):
                print('RAISE EXCEPTION')
            if not first:
                query += ' and '
            else:
                query += ' where '
                first = False
            query += 'c.sex in (\''+sexes.pop()[0]+'\''
            for sex in sexes:
                query += ', \'' + sex + '\''
            query += ')'

        if request.POST.getlist('tracks'):
            shapes = request.POST.getlist('tracks')
            if not first:
                query += ' and '
            else:
                query += ' where '
                first = False
            try:
                query += 't.id in ('+str(int(shapes.pop()[0]))
                for shape in shapes:
                    query += ', ' + str(int(shape))
            except ValueError:
                print('RAISE EXCEPTION')
            query += ')'

        if request.POST.getlist('seats'):
            no_of_seats = request.POST.getlist('seats')
            if not first:
                query += ' and '
            else:
                query += ' where '
                first = False
            try:
                query += 'km.number_of_seats in ('+str(no_of_seats.pop()[0])
                for no in no_of_seats:
                    query += ', ' + str(no)
            except ValueError:
                print('RAISE EXCEPTION')
            query += ')'

    query += ' and l.end_time is not null order by time limit 20'
    records = Lap.objects.raw(query)
    
    for i in range(0,len(records)):
        print(records[i].time)
        records[i].time = datetime.datetime.fromtimestamp(records[i].time/1000).strftime('%M:%S.%f')[:-3]
    return records


def getDate(request):
    date = []
    if request.method == 'POST':
        if request.POST.getlist('date'):
            date = request.POST.getlist('date')
            print(date)

        dates = Race.objects.raw(
            'select id, date, number from race where date = %s', tuple(date))
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

        drivers = RaceDrivers.objects.raw(
            'select * from race_drivers rd inner join race r on rd.race_id=r.id where r.id = %s', [numbers])

        for rd in drivers:
            times = Lap.objects.raw(
                'select l.id, l.end_time-l.start_time as "time" from lap l inner join race_drivers rd on l.race_drivers_id=rd.id inner join client c on rd.client_id=c.id where l.race_drivers_id = %s order by l.id', [rd.id])
            race_info = RaceDrivers.objects.raw(
                'select rd.id, avg(l.end_time-l.start_time) as "mean", max(l.end_time-l.start_time) as "worst", min(l.end_time-l.start_time) as "best", c.name from race_drivers rd inner join lap l on l.race_drivers_id=rd.id inner join client c on rd.client_id=c.id where l.race_drivers_id = %s group by rd.id', [rd.id])

            if len(times) > temp_lent:
                temp_lent = len(times)

            base = [race_info[0].name, race_info[0].best,
                    race_info[0].worst, round(race_info[0].mean)]

            for i in range(1, len(base)):
                base[i] = datetime.datetime.fromtimestamp(
                    base[i]/1000).strftime('%M:%S.%f')[:-3]

            x = [datetime.datetime.fromtimestamp(
                i.time/1000).strftime('%M:%S.%f')[:-3] for i in times]
            full.append(base + x)

            x_for_plot = [i.time for i in times]
            full_for_plot.append([race_info[0].name, race_info[0].best,
                                  race_info[0].worst, race_info[0].mean] + x_for_plot)

        lent = ['#' + str(i) for i in range(1, temp_lent+1)]
        first_col = ['Name', 'Best time', 'Worst time', 'Mean time'] + lent
        full.insert(0, first_col)
        full_for_plot.insert(0, first_col)

        return full, full_for_plot


def plot(request):
    y = []
    x = []
    title = []
    _, axis = displayRaces(request)
    for i in range(1, len(axis)):
        y.append(axis[i][4:])
        x.append([i for i in range(1, len(y[i-1])+1)])
        title.append(axis[i][0])

    fig = make_subplots(x_title='Lap number', y_title='Time in milliseconds')
    colors = ["#800000", "#FF0000", "#800080", "#FF00FF", "#008000",
              "#00FF00", "#808000", "#000080", "#0000FF", "#008080", "#00FFFF"]
    for i in range(0, len(title)):
        fig.add_trace(go.Scatter(
            x=x[i], y=y[i], mode='lines', name=title[i], opacity=0.8, marker_color=colors[i]))

    updatemenus=list([
    dict(
        buttons=[],
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0,
        xanchor = 'left',
        y = 1.2,
        yanchor = 'top'
        ),
    ])

    lister = []
    for k in range(0,len(title)):
        lister.append(dict(
            args=['visible', [True for k in range(0,len(title))] if k == 0 else [True if (i+1) == k else False for i in range(0,len(title))]],
            label=str( 'All' if k == 0 else title[k]),
            method='restyle'
        ))

    updatemenus[0]['buttons'] = lister

    fig['layout']['updatemenus'] = updatemenus

    return fig.to_html(full_html=False, include_plotlyjs='cdn', default_height=800, default_width=1200)


def register(request):
    form = SignUpForm(request.POST)
    print(form.errors.as_data())
    if form.is_valid():
        user = form.save(commit=False)
        to_email = form.cleaned_data.get('email')
        user.is_active = False
        clients = Client.objects.raw(
            'select * from client c where c.email=%s', [user.email])
        if clients:
            client = clients[0]
            client.user = user
            user.client = client
        else:
            user.client=Client(user=user, email=to_email)     

        user.save()
            
        

        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('registration/activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        
        email = EmailMessage(mail_subject, message, to=[to_email])
        print('test')
        email.send()
        
        return HttpResponse('Please confirm your email address to complete the registration')
    else:
        return HttpResponseBadRequest('Bad request - username or email already taken')


def activate_user(request, uidb64, token):
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




      
