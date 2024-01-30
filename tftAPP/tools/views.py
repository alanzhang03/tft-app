from django.shortcuts import render

def tools_view(request):
    return render(request, 'tools.html')
