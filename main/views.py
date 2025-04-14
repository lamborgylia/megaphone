from django.shortcuts import render
from .models import Tariff

def index(request):
    return render(request, 'index.html')

def index(request):
    tariffs = Tariff.objects.all().order_by('order')
    return render(request, "index.html", {"tariffs": tariffs})
