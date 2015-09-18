from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Duy Anh says hello to all of you guys! ;-)</h1> <a href='about/'>About page</a>")

def about(request):
    return HttpResponse("<h2>Rango says here is the about page.</h2> <a href='..'>Homepage</a>")