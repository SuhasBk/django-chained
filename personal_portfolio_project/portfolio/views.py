from django.shortcuts import render
from django.conf import settings
from .models import Project

# Create your views here.
def home(request):
    projects = Project.objects.all()
    return render(request,"portfolio/home.html",{'projects':projects})