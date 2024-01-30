from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def comps_view(request):
    return render(request, 'comps.html')