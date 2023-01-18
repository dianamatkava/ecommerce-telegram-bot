from django.http import HttpResponse
from django.shortcuts import render
from .tasks import updateCategories
# Create your views here.

def home(request):
    # updateCategories()
    return HttpResponse('')