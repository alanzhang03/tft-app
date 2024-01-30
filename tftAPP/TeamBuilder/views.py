from django.shortcuts import render

def teamBuilder_view(request):
    return render(request, 'teamBuilder.html')
