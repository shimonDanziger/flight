from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight


def index(request):
    return render(request, "myapp/index.html", {

        "flights_depart": list(Flight.objects.values_list('segmentsDepartureAirportCode', flat=True).distinct()),
        "flights_arrival": list(Flight.objects.values_list('segmentsArrivalAirportCode', flat=True).distinct())


    })  