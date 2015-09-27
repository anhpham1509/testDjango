__author__ = 'DuyAnhPham'

from django.http import HttpResponse

def homepage(request):
    return HttpResponse("This is homepage<br/><a href='/rango/'>Rango Project</a>")