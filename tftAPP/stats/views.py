from django.http import HttpResponse
from . models import Augment
from django.shortcuts import render


def stats_view(request):
    all_augs = Augment.objects.all()
    context = {'all_augs': all_augs}
    return render(request, 'stats.html', context)