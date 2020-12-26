from django.shortcuts import render
from django.http import HttpResponse
from aghart.models import KartModel
# Create your views here.
models = []
models = [p.name for p in KartModel.objects.raw('SELECT id,name FROM kart_model')]

def home(request):
    return render(request, 'aghart/home.html')

def records(request):
    return render(request, 'aghart/records.html', {'models': models})

def statistics(request):
    return render(request, 'aghart/statistics.html')