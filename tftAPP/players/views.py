from django.shortcuts import render

def players_view(request):
    return render(request, 'players.html')
