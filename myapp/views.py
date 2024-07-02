from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight


def index(request):
    return render(request, "myapp/index.html", {

        "flights": Flight.objects.all()
    })