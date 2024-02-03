from django.http import HttpResponse
from . models import Augment
from django.shortcuts import render


def stats_view(request):
    all_augs = Augment.objects.all()
    context = {'all_augs': all_augs}
    return render(request, 'stats.html', context)




from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import os

# def download_file(request):
#     return render(request, 'riot.html')

def download_file(request):
    # print(os.getcwd())
    with open('stats/static/riot.txt') as file:
        response = HttpResponse(file.read(), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=riot.txt'
        return response