from django.http import HttpResponse
from django.shortcuts import render

from .models import User, Rent, Entry

def index(request):
    rent = Rent.objects.first().amount
    return render(request, 'rentsplitter/index.html')
