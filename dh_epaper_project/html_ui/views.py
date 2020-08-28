from django.shortcuts import render
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
import os

# Create your views here.
def deccan(request):
    return render(request, "deccan.html")

def locate_epaper(request):
    file_name = request.GET.get('file')
    try:
        return FileResponse(open(file_name, "rb"), content_type='application/pdf')
    except:
        return HttpResponseRedirect("/")
