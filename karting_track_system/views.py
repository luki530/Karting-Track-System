from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from karting_track_system.models import KartModel
# Create your views here.
models = []

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def my_custom_sql(self):
    models = [p.model for p in KartModel.objects.raw('select id, model from kart_model')]
        
    return models

def home(request):
    return render(request, 'karting_track_system/home.html')

def records(request):
    return render(request, 'karting_track_system/records.html', {'models': my_custom_sql(models)}) #,'sexes':['M','F']

def statistics(request):
    return render(request, 'karting_track_system/statistics.html')


def generateRecords(request):
    if request.method=='POST':
        if request.POST.getlist('kart_models'):
            modelsPost = KartModel()
            modelsPost.model = request.POST.getlist('kart_models')
            print(modelsPost.model)
        # elif request.POST.getlist('sexes'):
        #     sexesPost = Client()
        #     sexesPost.sex = request.POST.getlist('sexes')
        #     print(sexesPost.sex)
    return render(request, 'karting_track_system/records.html')