"""
URL configuration for tftAPP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from stats import views as stats_views
from home import views as home_views
# from comps import views as comps_views
# from players import views as players_views
# from teamBuilder import views as teamBuilder_views
# from tools import views as tools_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_views.home_view),
    # path("comps/", comps_views.comps_view),
    path("stats/", stats_views.stats_view),
    # path("players/", players_views.players_view),
    # path("tools/", tools_views.tools_view),
    # path("TeamBuilder/", teamBuilder_views.teamBuilder_view),
    # path('stats//riot.txt', stats_views.download_file),
    
]
    
