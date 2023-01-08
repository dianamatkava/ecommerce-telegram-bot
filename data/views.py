from django.shortcuts import render
from tasks import *
# Create your views here.

def home(request):
    updateCategories()