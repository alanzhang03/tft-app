from django.http import HttpResponse
from django.shortcuts import render


def TeamBuilder_views(request):
    return render(request, 'TeamBuilder.html')
