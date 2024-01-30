from django.http import HttpResponse
from django.shortcuts import render


def comps_view(request):
    return render(request, 'comps.html')
