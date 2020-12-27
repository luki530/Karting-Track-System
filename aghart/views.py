from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
models = []
def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM kart_model")
        models = [item[0] for item in cursor.fetchall()]
    return models

def home(request):
    return render(request, 'aghart/home.html')

def records(request):
    return render(request, 'aghart/records.html', {'models': my_custom_sql(models)})

def statistics(request):
    return render(request, 'aghart/statistics.html')

